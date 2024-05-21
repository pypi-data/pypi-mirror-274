import os

import numpy as np
import xmltodict
from yt.utilities.io_handler import BaseIOHandler

from .util import _valid_element_mask, decode_binary, decode_piece, type_decider


class IOHandlerPVTU(BaseIOHandler):
    _particle_reader = False
    _dataset_type = "pvtu"
    _INDEX_OFFSET = 1
    _vector_fields = ("Coordinates", "velocity")
    _xyz_to_dim = {"x": 0, "y": 1, "z": 2}
    _vel_vectors = ["velocity_" + dim for dim in ["x", "y", "z"]]

    def __init__(self, ds):
        self.filename = ds.index_filename
        super().__init__(ds)
        self.node_fields = ds._get_nod_names()
        self.elem_fields = ds._get_elem_names()
        self._detect_null_elements = ds._detect_null_elements

    def _read_fluid_selection(self, chunks, selector, fields, size):
        # This needs to allocate a set of arrays inside a dictionary, where the
        # keys are the (ftype, fname) tuples and the values are arrays that
        # have been masked using whatever selector method is appropriate.  The
        # dict gets returned at the end and it should be flat, with selected
        # data.  Note that if you're reading grid data, you might need to
        # special-case a grid selector object.

        # always select all since these are chunks of a single mesh...
        ftype_list = []
        rv = {}
        for field in fields:
            ftype, fname = field
            rv[field] = []
            ftype_list.append(ftype)

        for chunk_id, chunk in enumerate(chunks):
            mesh = chunk.objs[0]
            npc = mesh.nodes_per_cell
            el_counts = np.array(mesh.element_count)

            # for now, we have all file info in single chunk
            mesh_name = f"connect{chunk_id}"
            if "all" in ftype_list or mesh_name in ftype_list:
                # mask here is the **element** mask. i.e.,
                #     shape(mask) = (n_elments,)
                # rather than (n_elements, n_verts). These apply to all fields,
                # so pull them out here:
                mask = selector.fill_mesh_cell_mask(mesh)  # global mask
                if mask is not None:
                    # each mesh piece will pull the connectivity, mask values
                    # for the indices corresponding to each vtu file
                    for vtu_id, vtu_fi in enumerate(mesh.filenames):
                        # the element mask for this piece
                        element_offset_start = el_counts[0:vtu_id].sum()
                        element_offset_end = element_offset_start + el_counts[vtu_id]
                        vtu_mask = mask[element_offset_start:element_offset_end]

                        # load this vtu's part of the mesh
                        vtu_file = os.path.join(self.ds.data_dir, vtu_fi)
                        f2id = self.ds.parameters["field_to_piece_index"][vtu_file]
                        with open(vtu_file) as data:
                            xml = xmltodict.parse(data.read())
                            xmlPieces = xml["VTKFile"]["UnstructuredGrid"]["Piece"]

                        if not isinstance(xmlPieces, list):
                            xmlPieces = [xmlPieces]

                        for field in fields:
                            ftype, fname = field

                            # check if we are dealing with a velocity component
                            vdim = -1
                            if fname in self._vel_vectors:
                                vdim = self._xyz_to_dim[fname.split("_")[-1]]
                                fname = "velocity"

                            vtu_field = self._read_single_vtu_field(
                                xmlPieces, fname, f2id, npc, vectordim=vdim
                            )
                            vtu_field = vtu_field[vtu_mask, :]
                            rv[field].append(vtu_field)

        for field in fields:
            rv[field] = np.concatenate(rv[field]).astype(np.float64)

        return rv

    def _read_single_vtu_field(
        self,
        xmlPieces,
        fieldname,
        field_to_piece_index,
        npc,
        vectordim=-1,
        ndims=3,
    ):
        # xmlPieces : the vtu file pieces (not de-coded)
        # fieldname : the field to fetch
        # field_to_piece_index : the index of the field within a single xmlPiece array
        # npc : nodes per cell
        vtu_data = []
        pieceoff = 0
        vtu_conns = []

        for piece_id in range(0, len(xmlPieces)):
            field_id = field_to_piece_index[piece_id][fieldname]
            xmlPiece = xmlPieces[piece_id]
            data_array = xmlPiece["PointData"]["DataArray"][field_id]
            names = data_array["@Name"]
            if names == fieldname:
                types = type_decider[data_array["@type"]]
                metadata, data_field = decode_binary(
                    data_array["#text"].encode(), dtype=types
                )
                if vectordim >= 0:
                    # extract the dimension of the vector we want
                    data_field = data_field.reshape((data_field.size // ndims, ndims))
                    data_field = data_field[:, vectordim]
                vtu_data.append(data_field.astype(np.float64))

            coords, conn, offsets, cell_types = decode_piece(xmlPieces[piece_id])
            vtu_conns.extend(conn + pieceoff)
            # the connectivity array can repeat index references to coordinates
            # update the offset number by the number of coords points:
            pieceoff = pieceoff + coords.shape[0]

        vtu_data = np.concatenate(vtu_data)
        vtu_conns = np.array(vtu_conns)  # 1D connectivity

        vtu_data = vtu_data[vtu_conns]  # 1D data array
        vtu_data = vtu_data.reshape((vtu_conns.size // npc, npc))

        if self._detect_null_elements:
            vtu_conns = vtu_conns.reshape((vtu_conns.size // npc, npc))
            valid_elements, n_invalid = _valid_element_mask(vtu_conns)
            if n_invalid > 0:
                return vtu_data[valid_elements, :]

        return vtu_data


class IOHandlerASPECT(IOHandlerPVTU):
    _dataset_type = "aspect"

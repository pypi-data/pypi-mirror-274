import unittest
import os
import filecmp
import gmsh
import logging
import shutil
from typing import Union, Tuple, Literal
import ruamel.yaml
import numpy as np

from fiqus.data.DataFiQuS import FDM
from fiqus.MainFiQuS import MainFiQuS
from fiqus.utils.Utils import GmshUtils
from fiqus.parsers.ParserMSH import ParserMSH
from fiqus.utils.Utils import FilesAndFolders as FFs

logger = logging.getLogger(__name__)


class BaseClassesForTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Change the working directory to the directory where this file's parent
        # directory is located (tests folder):
        os.chdir(os.path.dirname(os.path.dirname(__file__)))
        cls.inputs_folder = os.path.join(os.getcwd(), "_inputs")
        cls.outputs_folder = os.path.join(os.getcwd(), "_outputs")
        cls.references_folder = os.path.join(os.getcwd(), "_references")

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        """
        This method is executed before each test in this class.

        It changes the working directory to the directory where this file is located.
        """
        # Change the working directory to the directory where this file's parent
        # directory is located (tests folder):
        os.chdir(os.path.dirname(os.path.dirname(__file__)))

    def tearDown(self) -> None:
        pass

    def get_input_file_path(self, model_name: str) -> Union[str, os.PathLike]:
        """
        This method returns the path to the input file for the given model name.

        :param model_name: name of the model to get the input file for
        :type model_name: str
        :return: path to the input file
        :rtype: Union[str, os.PathLike]
        """
        return os.path.join(self.inputs_folder, f"{model_name}", f"{model_name}.yaml")

    def get_data_model(self, model_name: str) -> FDM:
        """
        This method returns the data model for the given model name by reading the
        input file.

        :param model_name: name of the model to get the data model for
        :type model_name: str
        :return: data model
        :rtype: FDM
        """
        input_file_path = self.get_input_file_path(model_name)

        # Read and prepare the input file:
        fdm = FFs.read_data_from_yaml(input_file_path, FDM)

        if fdm.run.geometry is None:
            fdm.run.geometry = 1
        if fdm.run.mesh is None:
            fdm.run.mesh = 1
        if fdm.run.solution is None:
            fdm.run.solution = 1

        return fdm

    def run_fiqus(
        self,
        data_model: FDM,
        model_name: str,
        run_type: Literal[
            "start_from_yaml",
            "mesh_only",
            "geometry_only",
            "geometry_and_mesh",
            "pre_process_only",
            "mesh_and_solve_with_post_process_python",
            "solve_with_post_process_python",
            "solve_only",
            "post_process_getdp_only",
            "post_process_python_only",
        ],
    ) -> None:
        """
        This method runs FiQuS with the given model name and run type.

        :param model_name: name of the model to run FiQuS for
        :type model_name: str
        :param run_type: run type to run FiQuS with
        :type run_type: Literal[
                "start_from_yaml",
                "mesh_only",
                "geometry_only",
                "geometry_and_mesh",
                "pre_process_only",
                "mesh_and_solve_with_post_process_python",
                "solve_with_post_process_python",
                "solve_only",
                "post_process_getdp_only",
                "post_process_python_only",
            ]
        """
        # Make sure the run type is correct:
        data_model.run.type = run_type

        # Make sure the output files are overwritten:
        data_model.run.overwrite = True

        # Disable GUI:
        data_model.run.launch_gui = False

        # Prepare the output folder:
        model_folder = os.path.join(self.outputs_folder, f"{model_name}_{run_type}")
        FFs.prep_folder(model_folder)

        # Depending on the run_type, copy the reference files to the model folder:
        if run_type in ["geometry_only", "geometry_and_mesh", "start_from_yaml"]:
            pass
        else:
            # Copy the reference geometry and mesh folders to the model folder:
            reference_geometry_folder = self.get_path_to_specific_reference_folder(
                data_model, model_name, folder="Geometry"
            )
            reference_mesh_folder = self.get_path_to_specific_reference_folder(
                data_model, model_name, folder="Mesh"
            )

            output_geometry_folder = self.get_path_to_specific_output_folder(
                data_model, model_name, run_type=run_type, folder="Geometry"
            )
            output_mesh_folder = self.get_path_to_specific_output_folder(
                data_model, model_name, run_type=run_type, folder="Mesh"
            )

            shutil.copytree(
                reference_geometry_folder, output_geometry_folder, dirs_exist_ok=True
            )
            shutil.copytree(
                reference_mesh_folder, output_mesh_folder, dirs_exist_ok=True
            )

        # Run FiQuS:
        MainFiQuS(
            model_folder=model_folder,
            input_file_path=self.get_input_file_path(model_name),
            fdm=data_model,
            verbose=False,
        )

    def get_path_to_generated_file(
        self,
        data_model: FDM,
        model_name: str,
        file_name: str,
        file_extension: str,
        run_type: Literal[
            "start_from_yaml",
            "mesh_only",
            "geometry_only",
            "geometry_and_mesh",
            "pre_process_only",
            "mesh_and_solve_with_post_process_python",
            "solve_with_post_process_python",
            "solve_only",
            "post_process_getdp_only",
            "post_process_python_only",
        ],
    ) -> Union[str, os.PathLike]:
        """
        This method returns the path to the generated file with the given extension
        for the given model name depending on the run type.

        :param model_name: name of the model to get the generated file for
        :type model_name: str
        :param file_name: name of the file
        :type file_name: str
        :param file_extension: file extension of the generated file
        :type file_extension: str
        :param run_type: run type to run FiQuS with
        :type run_type: Literal[
                "start_from_yaml",
                "mesh_only",
                "geometry_only",
                "geometry_and_mesh",
                "pre_process_only",
                "mesh_and_solve_with_post_process_python",
                "solve_with_post_process_python",
                "solve_only",
                "post_process_getdp_only",
                "post_process_python_only",
            ]
        :return: path to the generated file
        :rtype: Union[str, os.PathLike]
        """
        if run_type == "geometry_only":
            folder = "Geometry"
        elif run_type == "mesh_only":
            folder = "Mesh"
        elif run_type == "solve_only":
            folder = "Solution"
        else:
            raise ValueError(
                "The run type must be geometry_only, mesh_only, or solve_only!"
            )

        sections_folder = self.get_path_to_specific_output_folder(
            data_model, model_name, run_type, folder
        )

        generated_file = os.path.join(
            sections_folder,
            f"{file_name}.{file_extension}",
        )

        # Check if the file exists:
        if not os.path.isfile(generated_file):
            raise FileNotFoundError(
                f"Could not find the generated file: {generated_file}!"
            )

        return generated_file

    def get_path_to_specific_reference_folder(
        self,
        data_model: FDM,
        model_name: str,
        folder: Literal[
            "Geometry",
            "Mesh",
            "Solution",
        ],
    ):
        """
        This method returns the path to a specific reference folder (Geometry, Mesh, or
        Solution) for the given model name.

        :param model_name: name of the model to get the reference folder for
        :type model_name: str
        :param folder: folder to get the reference folder for
        :type folder: Literal[
                "Geometry",
                "Mesh",
                "Solution",
            ]
        """
        fdm = data_model
        geometry_folder_name = f"Geometry_{fdm.run.geometry}"
        mesh_folder_name = f"Mesh_{fdm.run.mesh}"
        solve_folder_name = f"Solution_{fdm.run.solution}"

        if folder == "Geometry":
            reference_folder = os.path.join(
                self.references_folder, model_name, geometry_folder_name
            )
        elif folder == "Mesh":
            reference_folder = os.path.join(
                self.references_folder,
                model_name,
                geometry_folder_name,
                mesh_folder_name,
            )
        elif folder == "Solution":
            reference_folder = os.path.join(
                self.references_folder,
                model_name,
                geometry_folder_name,
                mesh_folder_name,
                solve_folder_name,
            )

        return reference_folder

    def get_path_to_specific_output_folder(
        self,
        data_model: FDM,
        model_name: str,
        run_type: Literal[
            "start_from_yaml",
            "mesh_only",
            "geometry_only",
            "geometry_and_mesh",
            "pre_process_only",
            "mesh_and_solve_with_post_process_python",
            "solve_with_post_process_python",
            "solve_only",
            "post_process_getdp_only",
            "post_process_python_only",
        ],
        folder: Literal[
            "Geometry",
            "Mesh",
            "Solution",
        ],
    ):
        """
        This method returns a specific path (Geometry, Mesh, or Solution) to the output
        folder for the given model name depending on the run type.

        :param model_name: name of the model to get the output folder for
        :type model_name: str
        :param run_type: run type to run FiQuS with
        :type run_type: Literal[
                "start_from_yaml",
                "mesh_only",
                "geometry_only",
                "geometry_and_mesh",
                "pre_process_only",
                "mesh_and_solve_with_post_process_python",
                "solve_with_post_process_python",
                "solve_only",
                "post_process_getdp_only",
                "post_process_python_only",
            ]
        :param folder: folder to get the output folder for
        :type folder: Literal[
                "Geometry",
                "Mesh",
                "Solution",
            ]
        """
        fdm = data_model
        geometry_folder_name = f"Geometry_{fdm.run.geometry}"
        mesh_folder_name = f"Mesh_{fdm.run.mesh}"
        solve_folder_name = f"Solution_{fdm.run.solution}"

        if run_type is None:
            model_folder_name = model_name
        else:
            model_folder_name = f"{model_name}_{run_type}"

        if folder == "Geometry":
            output_folder = os.path.join(
                self.outputs_folder, model_folder_name, geometry_folder_name
            )
        elif folder == "Mesh":
            output_folder = os.path.join(
                self.outputs_folder,
                model_folder_name,
                geometry_folder_name,
                mesh_folder_name,
            )
        elif folder == "Solution":
            output_folder = os.path.join(
                self.outputs_folder,
                model_folder_name,
                geometry_folder_name,
                mesh_folder_name,
                solve_folder_name,
            )

        FFs.prep_folder(output_folder)

        return output_folder

    def get_path_to_reference_file(
        self,
        data_model: FDM,
        model_name: str,
        file_name: str,
        file_extension: str,
        folder: Literal[
            "Geometry",
            "Mesh",
            "Solution",
        ],
    ) -> Union[str, os.PathLike]:
        """
        This method returns the path to the reference file with the given extension
        for the given model name from the given folder.

        :param model_name: name of the model to get the reference file for
        :type model_name: str
        :param file_name: name of the model to get the reference file for
        :type file_name: str
        :param file_extension: file extension of the reference file
        :type file_extension: str
        :param folder: folder to get the reference file from
        :type folder: Literal[
                "Geometry",
                "Mesh",
                "Solution",
            ]
        :return: path to the reference file
        :rtype: Union[str, os.PathLike]
        """
        reference_folder = self.get_path_to_specific_reference_folder(
            data_model, model_name, folder=folder
        )
        reference_file = os.path.join(
            reference_folder,
            f"{file_name}.{file_extension}",
        )

        # Check if the file exists:
        if not os.path.isfile(reference_file):
            raise FileNotFoundError(
                f"Could not find the reference file: {file_name}.{file_extension}!"
            )

        return reference_file

    def compare_json_or_yaml_files(self, file_1, file_2):
        """
        This method compares the contents of two JSON or YAML files. It is used to
        check that the generated files are the same as the reference.

        :param file_1: path to the first file
        :type file_1: Union[str, os.PathLike]
        :param file_2: path to the second file
        :type file_2: Union[str, os.PathLike]
        """
        try:
            # YAML is a superset of JSON, so we can use the same parser for both:
            yaml = ruamel.yaml.YAML(typ="safe", pure=True)
            with open(file_1, "r") as file:
                file_1_dictionary = yaml.load(file)

            with open(file_2, "r") as file:
                file_2_dictionary = yaml.load(file)
        except:
            raise ValueError("The files must be JSON or YAML files!")

        # Compare the dictionaries:
        self.assertDictEqual(
            file_1_dictionary,
            file_2_dictionary,
            msg=f"{file_1} did not match {file_2}!",
        )

    def compare_pkl_files(self, file_1, file_2):
        """
        This method compares the contents of two pkl files. It is used to check that the
        generated files are the same as the reference.

        :param file_1: path to the first file
        :type file_1: Union[str, os.PathLike]
        :param file_2: path to the second file
        :type file_2: Union[str, os.PathLike]
        """
        # Compare the pickle files:
        self.assertTrue(
            filecmp.cmp(file_1, file_2),
            msg=f"{file_1} did not match {file_2}!",
        )

    def compare_text_files(self, file_1, file_2):
        """
        This method compares the contents of two files. It is used to check that the
        generated files are the same as the reference.

        :param file_1: path to the first file
        :type file_1: Union[str, os.PathLike]
        :param file_2: path to the second file
        :type file_2: Union[str, os.PathLike]
        """
        # Compare the files:
        self.assertTrue(
            filecmp.cmp(file_1, file_2),
            msg=f"{file_1} did not match {file_2}!",
        )


class FiQuSGeometryTests(BaseClassesForTests):
    def generate_geometry(
        self,
        data_model: FDM,
        model_name: str,
    ) -> Tuple[Union[str, os.PathLike], Union[str, os.PathLike]]:
        """
        This method generates the geometry for the given model name.

        :param data_model: data model to run FiQuS with
        :type data_model: FDM
        :param model_name: name of the model to generate the geometry for
        :type model_name: str
        :return: path to the generated geometry and volume information files
        :rtype: Tuple[Union[str, os.PathLike], Union[str, os.PathLike]]
        """
        self.run_fiqus(data_model, model_name, "geometry_only")
        self.model_name = model_name

    def compare_number_of_entities(
        self,
        geometry_file_1: Union[str, os.PathLike],
        geometry_file_2: Union[str, os.PathLike],
    ):
        """
        This method compares the number of entities for each dimension in two geometry
        files. It is used to check that the generated geometry file is the same as the
        reference.

        :param geometry_file_1: path to the first geometry file
        :type geometry_file_1: Union[str, os.PathLike]
        :param geometry_file_2: path to the second geometry file
        :type geometry_file_2: Union[str, os.PathLike]
        """
        # Initialize gmsh:
        gmsh_utils = GmshUtils(verbose=False)
        gmsh_utils.initialize()

        # Open the geometry files and get the entities:
        model_entities = {}
        for geometry_file in [geometry_file_1, geometry_file_2]:
            model_entities[geometry_file] = []

            gmsh.open(geometry_file)
            for dim in range(4):
                model_entities[geometry_file].append(
                    sorted(gmsh.model.getEntities(dim=dim))
                )
            gmsh.clear()

        # Compare the number of entities for each dimension:
        for dim in [0, 1, 2, 3]:
            self.assertEqual(
                len(model_entities[geometry_file_1][dim]),
                len(model_entities[geometry_file_2][dim]),
                msg=f"{geometry_file_1} and {geometry_file_2} did not match!",
            )

    def get_path_to_generated_file(
        self, data_model: FDM, file_name: str, file_extension: str
    ) -> Union[str, os.PathLike]:
        return super().get_path_to_generated_file(
            data_model,
            self.model_name,
            file_name,
            file_extension,
            run_type="geometry_only",
        )

    def get_path_to_reference_file(
        self, data_model: FDM, file_name: str, file_extension: str
    ) -> Union[str, os.PathLike]:
        return super().get_path_to_reference_file(
            data_model, self.model_name, file_name, file_extension, folder="Geometry"
        )


class FiQuSMeshTests(BaseClassesForTests):
    def generate_mesh(
        self,
        data_model: FDM,
        model_name: str,
    ) -> Tuple[Union[str, os.PathLike], Union[str, os.PathLike]]:
        """
        This method generates the mesh for the given model name.

        :param data_model: data model to run FiQuS with
        :type data_model: FDM
        :param model_name: name of the model to generate the mesh for
        :type model_name: str
        """
        self.run_fiqus(data_model, model_name, "mesh_only")
        self.model_name = model_name

    def compare_mesh_qualities(
        self, mesh_file_1: Union[str, os.PathLike], mesh_file_2: Union[str, os.PathLike]
    ):
        """
        This method compares the mesh qualities of two mesh files. It is used to check
        that the generated mesh file is the same as the reference.

        :param mesh_file_1: path to the first mesh file
        :type mesh_file_1: Union[str, os.PathLike]
        :param mesh_file_2: path to the second mesh file
        :type mesh_file_2: Union[str, os.PathLike]
        """
        # Initialize gmsh:
        gmsh_utils = GmshUtils(verbose=False)
        gmsh_utils.initialize()

        # Open the mesh files and get the average mesh quality:
        average_mesh_qualities = []
        for mesh_file in [mesh_file_1, mesh_file_2]:
            # Get physical group names:
            mesh = ParserMSH(mesh_file)
            average_mesh_qualities.append(mesh.get_average_mesh_quality())

        # Make sure the average mesh qualities are close enough:
        ratio = min(average_mesh_qualities) / max(average_mesh_qualities)
        self.assertGreater(
            ratio,
            0.9,
            msg=f"{mesh_file_1} and {mesh_file_2} did not match!",
        )

    def get_path_to_generated_file(
        self, data_model, file_name: str, file_extension: str
    ) -> Union[str, os.PathLike]:
        return super().get_path_to_generated_file(
            data_model, self.model_name, file_name, file_extension, run_type="mesh_only"
        )

    def get_path_to_reference_file(
        self, data_model, file_name: str, file_extension: str
    ) -> Union[str, os.PathLike]:
        return super().get_path_to_reference_file(
            data_model, self.model_name, file_name, file_extension, folder="Mesh"
        )


class FiQuSSolverTests(BaseClassesForTests):
    def solve(
        self,
        data_model: FDM,
        model_name: str,
    ) -> Tuple[Union[str, os.PathLike], Union[str, os.PathLike]]:
        """
        This method solves the given model name.

        :param data_model: data model to run FiQuS with
        :type data_model: FDM
        :param model_name: name of the model to generate the mesh for
        :type model_name: str
        """
        self.run_fiqus(data_model, model_name, "solve_only")
        self.model_name = model_name

    def compare_pos_files(
        self, pos_file_1: Union[str, os.PathLike], pos_file_2: Union[str, os.PathLike]
    ):
        """
        This method compares the contents of two pos files. It is used to check that
        the generated pos file is the same as the reference.

        :param pos_file_1: path to the first pos file
        :type pos_file_1: Union[str, os.PathLike]
        :param pos_file_2: path to the second pos file
        :type pos_file_2: Union[str, os.PathLike]
        """
        # Initialize gmsh:
        gmsh_utils = GmshUtils(verbose=False)
        gmsh_utils.initialize()

        # Open the pos files and get the model data:
        model_datas = []
        for pos_file in [pos_file_1, pos_file_2]:
            # Open the pos file:
            gmsh.open(pos_file)
            data_all_steps = []
            for time_step in range(1, 100):
                # Save all available time steps up to 100:
                try:
                    (
                        data_type,
                        tags,
                        data,
                        time,
                        numComponents,
                    ) = gmsh.view.getHomogeneousModelData(tag=0, step=time_step)
                    data_all_steps.extend(list(data))
                except:
                    break

            model_datas.append(data_all_steps)

        # Make sure the pos files are close enough:
        self.assertEqual(
            len(model_datas[0]),
            len(model_datas[1]),
            msg=f"{pos_file_1} and {pos_file_2} did not match!",
        )

        # Convert to numppy array:
        model_data1 = np.array(model_datas[0])
        model_data2 = np.array(model_datas[1])

        # Compare the data:
        np.testing.assert_allclose(
            model_data1,
            model_data2,
            rtol=1e-05,
            atol=1e-08,
        )

    def get_path_to_generated_file(
        self, data_model, file_name: str, file_extension: str
    ) -> Union[str, os.PathLike]:
        return super().get_path_to_generated_file(
            data_model,
            self.model_name,
            file_name,
            file_extension,
            run_type="solve_only",
        )

    def get_path_to_reference_file(
        self, data_model, file_name, file_extension
    ) -> Union[str, os.PathLike]:
        return super().get_path_to_reference_file(
            data_model, self.model_name, file_name, file_extension, folder="Solution"
        )

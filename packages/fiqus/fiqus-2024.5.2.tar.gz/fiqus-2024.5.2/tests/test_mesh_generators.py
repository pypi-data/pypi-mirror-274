import unittest
from tests.utils.fiqus_test_classes import FiQuSMeshTests

class TestMeshGenerators(FiQuSMeshTests):
    def test_Pancake3D(self):
        """
        Checks if Pancake3D geometry generators work correctly by comparing the number
        of entities in the generated geometry file to the reference file that was
        checked manually.
        """
        model_names = [
            "TEST_Pancake3D_REF",
            "TEST_Pancake3D_REFStructured",
            "TEST_Pancake3D_TSA",
            "TEST_Pancake3D_TSAStructured",
            "TEST_Pancake3D_TSAInsulating"
        ]

        for model_name in model_names:
            with self.subTest(model_name=model_name):
                data_model = self.get_data_model(model_name)

                # data_model can be modified here if necessary
                # Example:

                # data_model.magnet.mesh.wi.axne = 30

                self.generate_mesh(data_model, model_name)

                # Compare the number of entities with the reference file:
                mesh_file = self.get_path_to_generated_file(
                    data_model=data_model, file_name=model_name, file_extension="msh"
                )
                reference_file = self.get_path_to_reference_file(
                    data_model=data_model, file_name=model_name, file_extension="msh"
                )
                self.compare_mesh_qualities(mesh_file, reference_file)

                # Compare the regions files:
                regions_file = self.get_path_to_generated_file(
                    data_model=data_model,
                    file_name=model_name,
                    file_extension="regions",
                )
                reference_regions_file = self.get_path_to_reference_file(
                    data_model=data_model,
                    file_name=model_name,
                    file_extension="regions",
                )
                self.compare_json_or_yaml_files(regions_file, reference_regions_file)


if __name__ == "__main__":
    unittest.main()

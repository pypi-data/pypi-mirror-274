import unittest
from tests.utils.fiqus_test_classes import FiQuSGeometryTests


class TestGeometryGenerators(FiQuSGeometryTests):
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

                # data_model.magnet.geometry.N = 3

                self.generate_geometry(data_model, model_name)

                # Compare the number of entities with the reference file:
                geometry_file = self.get_path_to_generated_file(
                    data_model=data_model, file_name=model_name, file_extension="brep"
                )
                reference_file = self.get_path_to_reference_file(
                    data_model=data_model, file_name=model_name, file_extension="brep"
                )
                self.compare_number_of_entities(geometry_file, reference_file)

                # Compare the volume information files:
                vi_file = self.get_path_to_generated_file(
                    data_model=data_model, file_name=model_name, file_extension="vi"
                )
                reference_vi_file = self.get_path_to_reference_file(
                    data_model=data_model, file_name=model_name, file_extension="vi"
                )
                self.compare_json_or_yaml_files(vi_file, reference_vi_file)

if __name__ == "__main__":
    unittest.main()

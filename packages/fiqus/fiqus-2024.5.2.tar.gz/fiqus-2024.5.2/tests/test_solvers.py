import unittest
from tests.utils.fiqus_test_classes import FiQuSSolverTests
from fiqus.data.DataFiQuS import FDM
import fiqus.data.DataFiQuSPancake3D as Pancake3D


class TestSolvers(FiQuSSolverTests):
    def test_Pancake3D(self):
        """
        Checks if Pancake3D solvers work correctly by comparing the results to the
        reference results that were checked manually.
        """
        model_names = [
            "TEST_Pancake3D_REF",
            "TEST_Pancake3D_REFStructured",
            "TEST_Pancake3D_TSA",
            "TEST_Pancake3D_TSAStructured",
            "TEST_Pancake3D_TSAInsulating",
        ]
        solve_types = ["electromagnetic", "weaklyCoupled", "stronglyCoupled"]
        for model_name in model_names:
            for solve_type in solve_types:
                with self.subTest(model_name=model_name, solve_type=solve_type):
                    data_model: FDM = self.get_data_model(model_name)

                    data_model.magnet.solve.type = solve_type

                    data_model.run.solution = solve_type

                    if solve_type in ["weaklyCoupled", "stronglyCoupled"]:
                        data_model.magnet.solve.save = [
                            Pancake3D.Pancake3DSolveSaveQuantity(
                                quantity="magneticField",
                            ),
                            Pancake3D.Pancake3DSolveSaveQuantity(
                                quantity="currentDensity",
                            ),
                            Pancake3D.Pancake3DSolveSaveQuantity(
                                quantity="temperature",
                            ),
                        ]
                    elif solve_type == "electromagnetic":
                        data_model.magnet.solve.save = [
                            Pancake3D.Pancake3DSolveSaveQuantity(
                                quantity="magneticField",
                            ),
                            Pancake3D.Pancake3DSolveSaveQuantity(
                                quantity="currentDensity",
                            ),
                        ]

                    self.solve(data_model, model_name)

                    # Compare the pro files:
                    pro_file = self.get_path_to_generated_file(
                        data_model=data_model,
                        file_name=model_name,
                        file_extension="pro",
                    )
                    reference_pro_file = self.get_path_to_reference_file(
                        data_model=data_model,
                        file_name=model_name,
                        file_extension="pro",
                    )
                    self.compare_text_files(pro_file, reference_pro_file)

                    # Compare the results files:
                    pos_file = self.get_path_to_generated_file(
                        data_model=data_model,
                        file_name="MagneticField-DefaultFormat",
                        file_extension="pos",
                    )
                    reference_pos_file = self.get_path_to_reference_file(
                        data_model=data_model,
                        file_name="MagneticField-DefaultFormat",
                        file_extension="pos",
                    )
                    self.compare_pos_files(pos_file, reference_pos_file)

                    if solve_type in ["weaklyCoupled", "stronglyCoupled"]:
                        pos_file = self.get_path_to_generated_file(
                            data_model=data_model,
                            file_name="Temperature-DefaultFormat",
                            file_extension="pos",
                        )
                        reference_pos_file = self.get_path_to_reference_file(
                            data_model=data_model,
                            file_name="Temperature-DefaultFormat",
                            file_extension="pos",
                        )
                        self.compare_pos_files(pos_file, reference_pos_file)



if __name__ == "__main__":
    unittest.main()

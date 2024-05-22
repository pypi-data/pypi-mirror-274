//
// Created by whl on 24-5-21.
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "WinMLModel.h"
#include "WinMLSession.h"
#include "WinMLValue.h"

namespace py = pybind11;

// WinML 模型类包装
void init_winml(py::module &m) {
    py::enum_<winrt::Windows::AI::MachineLearning::LearningModelDeviceKind>(m, "DeviceType")
            .value("CPU", winrt::Windows::AI::MachineLearning::LearningModelDeviceKind::Cpu)
            .value("GPU", winrt::Windows::AI::MachineLearning::LearningModelDeviceKind::DirectXHighPerformance)
            .export_values();

    py::class_<WinMLModel>(m, "WinMLModel")
            .def(py::init<const std::wstring &>(), py::arg("model_path"))
            .def("get_model", &WinMLModel::GetModel)
            .def("get_author", &WinMLModel::GetAuthor)
            .def("get_name", &WinMLModel::GetName)
            .def("get_domain", &WinMLModel::GetDomain)
            .def("get_description", &WinMLModel::GetDescription)
            .def("get_input_names", &WinMLModel::GetInputNames)
            .def("get_output_names", &WinMLModel::GetOutputNames)
            .def("get_input_details", &WinMLModel::GetInputDetails)
            .def("get_output_details", &WinMLModel::GetOutputDetails);

    py::class_<WinMLSession>(m, "WinMLSession")
            .def(py::init<const WinMLModel &, winrt::Windows::AI::MachineLearning::LearningModelDeviceKind>(),
                 py::arg("model"),
                 py::arg("device_type") =
                 winrt::Windows::AI::MachineLearning::LearningModelDeviceKind::DirectXHighPerformance)
            .def("set_input", &WinMLSession::SetInput)
            .def("clear_input", &WinMLSession::ClearInput)
            .def("evaluate", &WinMLSession::Evaluate);

    py::class_<WinMLValue>(m, "WinMLValue")
            .def(py::init<const py::array &>(), py::arg("array"))
            .def("to_numpy", &WinMLValue::ToNumpyArray);
}

// 模块定义
PYBIND11_MODULE(winml, m) {
    m.doc() = "WinML Python bindings using pybind11";
    init_winml(m);
}

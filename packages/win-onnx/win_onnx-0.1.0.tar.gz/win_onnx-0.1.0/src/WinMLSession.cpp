//
// Created by whl on 24-5-21.
//
#include "WinMLSession.h"

using namespace winrt::Windows::AI::MachineLearning;

WinMLSession::WinMLSession(const WinMLModel &model, const LearningModelDeviceKind &device_kind): session_(nullptr) {
    session_ = LearningModelSession(model.GetModel(), LearningModelDevice(device_kind));
}

void WinMLSession::SetInput(const std::wstring &name, const WinMLValue &value) {
    inputs_[name] = value;
}

void WinMLSession::ClearInput() {
    inputs_.clear();
}

std::unordered_map<std::wstring, WinMLValue> WinMLSession::Evaluate() {
    LearningModelBinding binding(session_);

    // 绑定输入
    for (const auto &[name, value]: inputs_) {
        switch (value.GetTensorKind()) {
            case TensorKind::Float:
                binding.Bind(name, value.AsTensorFloat());
                break;
            case TensorKind::Int64:
                binding.Bind(name, value.AsTensorInt64());
                break;
            case TensorKind::UInt8:
                binding.Bind(name, value.AsTensorUInt8());
                break;
            case TensorKind::Float16:
                binding.Bind(name, value.AsTensorFloat16());
                break;
            case TensorKind::Double:
                binding.Bind(name, value.AsTensorDouble());
                break;
            case TensorKind::Int8:
                binding.Bind(name, value.AsTensorInt8());
                break;
            case TensorKind::UInt16:
                binding.Bind(name, value.AsTensorUInt16());
                break;
            case TensorKind::UInt32:
                binding.Bind(name, value.AsTensorUInt32());
                break;
            case TensorKind::UInt64:
                binding.Bind(name, value.AsTensorUInt64());
                break;
            case TensorKind::Int16:
                binding.Bind(name, value.AsTensorInt16());
                break;
            case TensorKind::Int32:
                binding.Bind(name, value.AsTensorInt32());
                break;
            default:
                throw std::runtime_error("Unsupported tensor kind");
        }
    }

    // 运行推理
    auto results = session_.Evaluate(binding, L"RunId");

    // 处理输出
    std::unordered_map<std::wstring, WinMLValue> outputs;
    for (const auto &output_name: session_.Model().OutputFeatures()) {
        auto output = results.Outputs().Lookup(output_name.Name()).as<ITensor>();
        if (output.Kind() == LearningModelFeatureKind::Tensor) {
            auto tensor = output;
            auto shape = tensor.Shape();
            std::vector<int64_t> np_shape(shape.begin(), shape.end());

           if (tensor.TensorKind() == TensorKind::Float) {
                auto data = tensor.as<TensorFloat>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<float>(np_shape, reinterpret_cast<float*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::Int64) {
                auto data = tensor.as<TensorInt64Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<int64_t>(np_shape, reinterpret_cast<int64_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::UInt8) {
                auto data = tensor.as<TensorUInt8Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<uint8_t>(np_shape, reinterpret_cast<uint8_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::Float16) {
                auto data = tensor.as<TensorFloat16Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<float>(np_shape, reinterpret_cast<float*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::Double) {
                auto data = tensor.as<TensorDouble>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<double>(np_shape, reinterpret_cast<double*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::Int8) {
                auto data = tensor.as<TensorInt8Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<int8_t>(np_shape, reinterpret_cast<int8_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::UInt16) {
                auto data = tensor.as<TensorUInt16Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<uint16_t>(np_shape, reinterpret_cast<uint16_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::UInt32) {
                auto data = tensor.as<TensorUInt32Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<uint32_t>(np_shape, reinterpret_cast<uint32_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::UInt64) {
                auto data = tensor.as<TensorUInt64Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<uint64_t>(np_shape, reinterpret_cast<uint64_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::Int16) {
                auto data = tensor.as<TensorInt16Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<int16_t>(np_shape, reinterpret_cast<int16_t*>(data)));
            }
            else if (tensor.TensorKind() == TensorKind::Int32) {
                auto data = tensor.as<TensorInt32Bit>().CreateReference().data();
                outputs[std::wstring(output_name.Name())] =
                    WinMLValue(pybind11::array_t<int32_t>(np_shape, reinterpret_cast<int32_t*>(data)));
            }
        }
    }

    return outputs;
}

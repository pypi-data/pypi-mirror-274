//
// Created by whl on 24-5-21.
//

#include "WinMLModel.h"

using namespace winrt::Windows::AI::MachineLearning;
using namespace winrt::Windows::Foundation::Collections;
using namespace winrt::Windows::Foundation;

WinMLModel::WinMLModel(const std::wstring &model_path): model_(nullptr) {
    winrt::init_apartment();
    model_ = LearningModel::LoadFromFilePath(model_path);
}

LearningModel WinMLModel::GetModel() const {
    return model_;
}

std::string WinMLModel::GetAuthor() const {
    return winrt::to_string(model_.Author());
}

std::string WinMLModel::GetName() const {
    return winrt::to_string(model_.Name());
}

std::string WinMLModel::GetDomain() const {
    return winrt::to_string(model_.Domain());
}

std::string WinMLModel::GetDescription() const {
    return winrt::to_string(model_.Description());
}

std::vector<std::string> WinMLModel::GetInputNames() const {
    std::vector<std::string> input_names;
    // const auto f = model_.InputFeatures();
    // const auto v = std::vector<ILearningModelFeatureDescriptor>{f.begin(), f.end()};
    for (const auto &feature: model_.InputFeatures()) {
        input_names.push_back(winrt::to_string(feature.Name()));
    }
    return input_names;
}

std::vector<std::string> WinMLModel::GetOutputNames() const {
    std::vector<std::string> output_names;
    for (const auto &feature: model_.OutputFeatures()) {
        output_names.push_back(winrt::to_string(feature.Name()));
    }
    return output_names;
}

std::vector<std::tuple<std::string, std::vector<int64_t>, std::string> > WinMLModel::GetInputDetails() const {
    std::vector<std::tuple<std::string, std::vector<int64_t>, std::string> > input_details;
    for (const auto &feature: model_.InputFeatures()) {
        auto tensor_feature = feature.as<TensorFeatureDescriptor>();
        if (tensor_feature) {
            std::string name = winrt::to_string(tensor_feature.Name());
            std::vector<int64_t> shape(tensor_feature.Shape().begin(), tensor_feature.Shape().end());
            std::string dtype = GetDataType(tensor_feature.TensorKind());
            input_details.emplace_back(name, shape, dtype);
        }
    }
    return input_details;
}

std::vector<std::tuple<std::string, std::vector<int64_t>, std::string> > WinMLModel::GetOutputDetails() const {
    std::vector<std::tuple<std::string, std::vector<int64_t>, std::string> > output_details;
    for (const auto &feature: model_.OutputFeatures()) {
        auto tensor_feature = feature.as<TensorFeatureDescriptor>();
        if (tensor_feature) {
            std::string name = winrt::to_string(tensor_feature.Name());
            std::vector<int64_t> shape(tensor_feature.Shape().begin(), tensor_feature.Shape().end());
            std::string dtype = GetDataType(tensor_feature.TensorKind());
            output_details.emplace_back(name, shape, dtype);
        }
    }
    return output_details;
}

std::string WinMLModel::GetDataType(TensorKind tensor_kind) const {
    switch (tensor_kind) {
        case TensorKind::Float: return "float32";
        case TensorKind::UInt8: return "uint8";
        case TensorKind::Int8: return "int8";
        case TensorKind::UInt16: return "uint16";
        case TensorKind::Int16: return "int16";
        case TensorKind::Int32: return "int32";
        case TensorKind::Int64: return "int64";
        case TensorKind::String: return "string";
        case TensorKind::Boolean: return "bool";
        case TensorKind::Float16: return "float16";
        case TensorKind::Double: return "float64";
        case TensorKind::UInt32: return "uint32";
        case TensorKind::UInt64: return "uint64";
        case TensorKind::Complex64: return "complex64";
        case TensorKind::Complex128: return "complex128";
        default: return "unknown";
    }
}

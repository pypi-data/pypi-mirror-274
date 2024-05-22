//
// Created by whl on 24-5-21.
//

#pragma once
#include <winrt/Windows.AI.MachineLearning.h>
#include <winrt/Windows.Foundation.h>
#include <winrt/windows.foundation.collections.h>
#include <string>

class WinMLModel {
public:
    WinMLModel(const std::wstring &model_path);

    winrt::Windows::AI::MachineLearning::LearningModel GetModel() const;

    std::string GetAuthor() const;

    std::string GetName() const;

    std::string GetDomain() const;

    std::string GetDescription() const;

    std::vector<std::string> GetInputNames() const;

    std::vector<std::string> GetOutputNames() const;

    std::vector<std::tuple<std::string, std::vector<int64_t>, std::string> > GetInputDetails() const;

    std::vector<std::tuple<std::string, std::vector<int64_t>, std::string> > GetOutputDetails() const;

private:
    winrt::Windows::AI::MachineLearning::LearningModel model_;
    std::string GetDataType(winrt::Windows::AI::MachineLearning::TensorKind tensor_kind) const;
};

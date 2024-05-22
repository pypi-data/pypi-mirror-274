//
// Created by whl on 24-5-21.
//

#pragma once
#include "WinMLModel.h"
#include <winrt/Windows.AI.MachineLearning.h>

#include "WinMLValue.h"

class WinMLSession {
public:
    WinMLSession(const WinMLModel &model,
                 const winrt::Windows::AI::MachineLearning::LearningModelDeviceKind &device_kind =
                         winrt::Windows::AI::MachineLearning::LearningModelDeviceKind::DirectXHighPerformance);

    void SetInput(const std::wstring& name, const WinMLValue& value);
    void ClearInput() ;
    std::unordered_map<std::wstring, WinMLValue> Evaluate();

private:
    winrt::Windows::AI::MachineLearning::LearningModelSession session_;
    std::unordered_map<std::wstring, WinMLValue> inputs_;
};

// Copyright (c) 2017-2025 The Khronos Group Inc.
//
// SPDX-License-Identifier: Apache-2.0

#include "pch.h"
#include "common.h"
#include "platformdata.h"
#include "platformplugin.h"
#include <android/native_activity.h>
#include <android/native_window.h>
#include <jni.h>

#ifdef XR_USE_PLATFORM_ANDROID

namespace {
struct AndroidPlatformPlugin : public IPlatformPlugin {
    AndroidPlatformPlugin(const std::shared_ptr<Options>& options, const std::shared_ptr<PlatformData>& data) 
        : m_options(options), m_data(data) {
        instanceCreateInfoAndroid = {XR_TYPE_INSTANCE_CREATE_INFO_ANDROID_KHR};
        instanceCreateInfoAndroid.applicationVM = data->applicationVM;
        instanceCreateInfoAndroid.applicationActivity = data->applicationActivity;
        
        // Request camera permissions for Mixed Reality
        RequestCameraPermissions();
    }

    std::vector<std::string> GetInstanceExtensions() const override { 
        return {XR_KHR_ANDROID_CREATE_INSTANCE_EXTENSION_NAME}; 
    }

    XrBaseInStructure* GetInstanceCreateExtension() const override { 
        return (XrBaseInStructure*)&instanceCreateInfoAndroid; 
    }

    void UpdateOptions(const std::shared_ptr<struct Options>& options) override {
        m_options = options;
    }

    void RequestCameraPermissions() {
        // This will be implemented to request camera permissions
        // For now, we'll add the basic structure
    }

    std::shared_ptr<Options> m_options;
    std::shared_ptr<PlatformData> m_data;
    XrInstanceCreateInfoAndroidKHR instanceCreateInfoAndroid;
};
}  // namespace

std::shared_ptr<IPlatformPlugin> CreatePlatformPlugin_Android(const std::shared_ptr<Options>& options,
                                                              const std::shared_ptr<PlatformData>& data) {
    return std::make_shared<AndroidPlatformPlugin>(options, data);
}
#endif

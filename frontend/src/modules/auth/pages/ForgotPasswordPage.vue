<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import AuthFormCard from "@/modules/auth/components/AuthFormCard.vue";
import ForgotPasswordForm from "@/modules/auth/components/ForgotPasswordForm.vue";
import { forgotPasswordPageConfig } from "@/modules/auth/utils/auth-page-content";
</script>

<template>
    <AuthLayout
        page-class="forgot-password-page"
        :intro="forgotPasswordPageConfig.intro"
    >
        <AuthFormCard
            :icon="forgotPasswordPageConfig.form.icon"
            :topline="forgotPasswordPageConfig.form.topline"
            :title="forgotPasswordPageConfig.form.title"
            :description="forgotPasswordPageConfig.form.description"
        >
            <ForgotPasswordForm />
        </AuthFormCard>
    </AuthLayout>
</template>

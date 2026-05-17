<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import AuthFormCard from "@/modules/auth/components/AuthFormCard.vue";
import ResetPasswordForm from "@/modules/auth/components/ResetPasswordForm.vue";
import { resetPasswordPageConfig } from "@/modules/auth/utils/auth-page-content";
</script>

<template>
    <AuthLayout
        page-class="reset-password-page"
        :intro="resetPasswordPageConfig.intro"
    >
        <AuthFormCard
            :icon="resetPasswordPageConfig.form.icon"
            :topline="resetPasswordPageConfig.form.topline"
            :title="resetPasswordPageConfig.form.title"
            :description="resetPasswordPageConfig.form.description"
        >
            <ResetPasswordForm />
        </AuthFormCard>
    </AuthLayout>
</template>
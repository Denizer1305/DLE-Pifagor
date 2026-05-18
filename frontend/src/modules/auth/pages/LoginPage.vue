<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import AuthFormCard from "@/modules/auth/components/AuthFormCard.vue";
import LoginForm from "@/modules/auth/components/LoginForm.vue";
import { loginPageConfig } from "@/modules/auth/utils/auth-page-content";
</script>

<template>
    <AuthLayout
        page-class="login-page"
        :intro="loginPageConfig.intro"
    >
        <AuthFormCard
            :icon="loginPageConfig.form.icon"
            :topline="loginPageConfig.form.topline"
            :title="loginPageConfig.form.title"
            :description="loginPageConfig.form.description"
        >
            <LoginForm />
        </AuthFormCard>
    </AuthLayout>
</template>

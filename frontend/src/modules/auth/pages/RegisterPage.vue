<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import AuthFormCard from "@/modules/auth/components/AuthFormCard.vue";
import RegisterForm from "@/modules/auth/components/RegisterForm.vue";
import { registerPageConfig } from "@/modules/auth/utils/auth-page-content";
</script>

<template>
    <AuthLayout
        page-class="register-page"
        :intro="registerPageConfig.intro"
    >
        <AuthFormCard
            :icon="registerPageConfig.form.icon"
            :topline="registerPageConfig.form.topline"
            :title="registerPageConfig.form.title"
            :description="registerPageConfig.form.description"
        >
            <RegisterForm />
        </AuthFormCard>
    </AuthLayout>
</template>

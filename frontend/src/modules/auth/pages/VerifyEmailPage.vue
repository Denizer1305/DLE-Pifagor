<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import AuthFormCard from "@/modules/auth/components/AuthFormCard.vue";
import VerifyEmailStatus from "@/modules/auth/components/VerifyEmailStatus.vue";
import { verifyEmailPageConfig } from "@/modules/auth/utils/auth-page-content";
</script>

<template>
    <AuthLayout
        page-class="verify-email-page"
        :intro="verifyEmailPageConfig.intro"
    >
        <AuthFormCard
            :icon="verifyEmailPageConfig.form.icon"
            :topline="verifyEmailPageConfig.form.topline"
            :title="verifyEmailPageConfig.form.title"
            :description="verifyEmailPageConfig.form.description"
        >
            <VerifyEmailStatus />
        </AuthFormCard>
    </AuthLayout>
</template>
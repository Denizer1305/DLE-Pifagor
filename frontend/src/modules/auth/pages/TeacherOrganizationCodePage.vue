<script setup lang="ts">
import AuthLayout from "@/layouts/AuthLayout.vue";
import AuthFormCard from "@/modules/auth/components/AuthFormCard.vue";
import TeacherOrganizationCodeForm from "@/modules/auth/components/TeacherOrganizationCodeForm.vue";
import { teacherOrganizationCodePageConfig } from "@/modules/auth/utils/auth-page-content";
</script>

<template>
    <AuthLayout
        page-class="teacher-organization-code-page"
        :intro="teacherOrganizationCodePageConfig.intro"
    >
        <AuthFormCard
            :icon="teacherOrganizationCodePageConfig.form.icon"
            :topline="teacherOrganizationCodePageConfig.form.topline"
            :title="teacherOrganizationCodePageConfig.form.title"
            :description="teacherOrganizationCodePageConfig.form.description"
        >
            <TeacherOrganizationCodeForm />
        </AuthFormCard>
    </AuthLayout>
</template>

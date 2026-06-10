<script setup lang="ts">
import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";
import { useDashboardLogout } from "@/composables/dashboard/useDashboardLogout";
import FeedbackRequestForm from "@/modules/feedback/components/FeedbackRequestForm.vue";
import { useFeedbackPage } from "@/modules/feedback/composables/useFeedbackPage";

const { logout } = useDashboardLogout();

const {
    content,
    errors,
    form,
    isSubmitted,
    isSubmitting,
    model,
    submitMessage,
    resetForm,
    removeFile,
    selectTopic,
    submitForm,
    updateFiles,
    updatePhone,
} = useFeedbackPage();
</script>

<template>
    <DashboardPageScaffold
        :model="model"
        :is-loading="false"
        error-message=""
        :loading-text="content.loadingText"
        :error-title="content.errorTitle"
        :retry-label="content.retryLabel"
        :retry-icon="content.retryIcon"
        @logout="logout"
    >
        <section class="feedback-page-hero fade-in visible">
            <div>
                <span class="dashboard-badge">
                    <i class="fas fa-headset"></i>
                    {{ content.hero.badge }}
                </span>

                <h1>{{ content.hero.title }}</h1>
                <p>{{ content.hero.text }}</p>
            </div>
        </section>

        <section class="feedback-page-grid">
            <article class="feedback-page-card feedback-page-info">
                <span class="dashboard-badge">
                    <i class="fas fa-circle-info"></i>
                    {{ content.info.title }}
                </span>
                <p>{{ content.info.text }}</p>

                <div class="feedback-page-info-list">
                    <div
                        v-for="item in content.info.items"
                        :key="item.title"
                        class="feedback-page-info-item"
                    >
                        <i :class="item.icon"></i>
                        <div>
                            <strong>{{ item.title }}</strong>
                            <span>{{ item.text }}</span>
                        </div>
                    </div>
                </div>
            </article>

            <article class="feedback-page-card">
                <FeedbackRequestForm
                    :content="content"
                    :errors="errors"
                    :form="form"
                    :is-submitted="isSubmitted"
                    :is-submitting="isSubmitting"
                    :submit-message="submitMessage"
                    @remove-file="removeFile"
                    @reset="resetForm"
                    @select-topic="selectTopic"
                    @submit="submitForm"
                    @update-files="updateFiles"
                    @update-phone="updatePhone"
                />
            </article>
        </section>
    </DashboardPageScaffold>
</template>

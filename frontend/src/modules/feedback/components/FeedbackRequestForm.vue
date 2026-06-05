<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import type {
    FeedbackFormErrors,
    FeedbackFormState,
    FeedbackPageContent,
} from "@/modules/feedback/types/feedback.types";

interface Props {
    content: FeedbackPageContent;
    errors: FeedbackFormErrors;
    form: FeedbackFormState;
    isSubmitted: boolean;
    isSubmitting: boolean;
    submitMessage: string;
}

defineProps<Props>();
const emit = defineEmits<{
    (event: "reset"): void;
    (event: "remove-file", index: number): void;
    (event: "select-topic", value: string): void;
    (event: "submit"): void;
    (event: "update-files", files: FileList | null): void;
    (event: "update-phone", value: string): void;
}>();
</script>

<template>
    <form
        class="feedback-page-form"
        @submit.prevent="emit('submit')"
    >
        <div class="feedback-page-section-head">
            <span class="dashboard-badge">
                <i class="fas fa-envelope-open-text"></i>
                {{ content.form.title }}
            </span>
            <p>{{ content.form.text }}</p>
        </div>

        <div class="feedback-page-form-grid">
            <label class="dashboard-create-field">
                <span>{{ content.form.nameLabel }}</span>
                <input
                    v-model="form.fullName"
                    type="text"
                    autocomplete="name"
                />
                <small v-if="errors.fullName">{{ errors.fullName }}</small>
            </label>

            <label class="dashboard-create-field">
                <span>{{ content.form.emailLabel }}</span>
                <input
                    v-model="form.email"
                    type="email"
                    autocomplete="email"
                />
                <small v-if="errors.email">{{ errors.email }}</small>
            </label>

            <label class="dashboard-create-field">
                <span>{{ content.form.phoneLabel }}</span>
                <input
                    :value="form.phone"
                    type="tel"
                    autocomplete="tel"
                    inputmode="tel"
                    placeholder="+7 900 000-00-00"
                    @input="emit('update-phone', ($event.target as HTMLInputElement).value)"
                />
                <small v-if="errors.phone">{{ errors.phone }}</small>
            </label>

            <label class="dashboard-create-field">
                <span>{{ content.form.organizationLabel }}</span>
                <input
                    v-model="form.organizationName"
                    type="text"
                    autocomplete="organization"
                />
                <small v-if="errors.organizationName">{{ errors.organizationName }}</small>
            </label>

            <div class="dashboard-create-field">
                <span>{{ content.form.topicLabel }}</span>
                <BaseSelect
                    id="feedback-page-topic"
                    :model-value="form.topic"
                    :options="content.topics"
                    :aria-label="content.form.topicLabel"
                    mode="overlay"
                    @update:model-value="emit('select-topic', $event)"
                />
                <small v-if="errors.topic">{{ errors.topic }}</small>
            </div>

            <label class="dashboard-create-field">
                <span>{{ content.form.subjectLabel }}</span>
                <input
                    v-model="form.subject"
                    type="text"
                    :placeholder="content.form.subjectPlaceholder"
                />
                <small v-if="errors.subject">{{ errors.subject }}</small>
            </label>

            <label class="dashboard-create-field is-wide">
                <span>{{ content.form.messageLabel }}</span>
                <textarea
                    v-model="form.message"
                    rows="7"
                    :placeholder="content.form.messagePlaceholder"
                ></textarea>
                <small v-if="errors.message">{{ errors.message }}</small>
            </label>

            <div class="dashboard-create-field feedback-page-files is-wide">
                <span>{{ content.form.filesLabel }}</span>

                <label class="feedback-page-file-picker">
                    <input
                        type="file"
                        multiple
                        accept=".jpg,.jpeg,.png,.webp,.pdf,.doc,.docx,image/jpeg,image/png,image/webp,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        @change="emit('update-files', ($event.target as HTMLInputElement).files)"
                    />
                    <i class="fas fa-paperclip"></i>
                    {{ content.form.filesButtonLabel }}
                </label>

                <p>{{ content.form.filesHint }}</p>

                <div
                    v-if="form.attachments.length"
                    class="feedback-page-file-list"
                >
                    <span
                        v-for="(file, index) in form.attachments"
                        :key="`${file.name}-${file.size}-${index}`"
                        class="feedback-page-file-chip"
                    >
                        <i class="fas fa-file-lines"></i>
                        {{ file.name }}
                        <button
                            type="button"
                            :aria-label="content.form.removeFileLabel"
                            @click="emit('remove-file', index)"
                        >
                            <i class="fas fa-xmark"></i>
                        </button>
                    </span>
                </div>

                <small v-if="errors.attachments">{{ errors.attachments }}</small>
            </div>

            <label class="feedback-page-consent is-wide">
                <input
                    v-model="form.isPersonalDataConsent"
                    type="checkbox"
                />
                <span>{{ content.form.consentLabel }}</span>
            </label>
            <small
                v-if="errors.isPersonalDataConsent"
                class="feedback-page-field-error is-wide"
            >
                {{ errors.isPersonalDataConsent }}
            </small>
        </div>

        <p
            v-if="errors.common"
            class="contact-form-error feedback-page-error"
        >
            {{ errors.common }}
        </p>

        <div
            v-if="isSubmitted"
            class="feedback-page-success"
        >
            <i class="fas fa-circle-check"></i>
            <div>
                <strong>{{ content.form.successTitle }}</strong>
                <span>{{ submitMessage || content.form.successText }}</span>
            </div>
        </div>

        <div class="feedback-page-actions">
            <button
                type="submit"
                class="dashboard-create-modal__primary"
                :disabled="isSubmitting"
            >
                <i :class="isSubmitting ? 'fas fa-spinner fa-spin' : 'fas fa-paper-plane'"></i>
                {{ isSubmitting ? content.form.submittingLabel : content.form.submitLabel }}
            </button>

            <button
                v-if="isSubmitted"
                type="button"
                class="dashboard-create-modal__secondary"
                @click="emit('reset')"
            >
                {{ content.form.resetLabel }}
            </button>
        </div>
    </form>
</template>

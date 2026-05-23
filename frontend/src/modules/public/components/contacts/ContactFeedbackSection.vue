<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from "vue";

import { useI18n } from "@/composables/useI18n";
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import { useContactFeedbackForm } from "@/modules/public/composables/useContactFeedbackForm";
import type {
    ContactFeedbackContent,
    ContactFeedbackTopic,
} from "@/modules/public/types/contact.types";

interface Props {
    content: ContactFeedbackContent;
}

const props = defineProps<Props>();
const { t } = useI18n();

const {
    form,
    errors,
    isSubmitting,
    isSubmitted,
    submitMessage,
    submitForm,
    resetForm,
    updateFiles,
} = useContactFeedbackForm();

const topicSelectRef = ref<HTMLElement | null>(null);
const isTopicSelectOpen = ref(false);
const topicSelectId = "contact-topic-select";

const selectedTopicLabel = computed(() => {
    const selectedTopic = props.content.topics.find((topic) => topic.value === form.topic);

    return selectedTopic?.label || props.content.fields.topic.label;
});

function closeTopicSelect() {
    isTopicSelectOpen.value = false;
}

function toggleTopicSelect() {
    isTopicSelectOpen.value = !isTopicSelectOpen.value;
}

function selectTopic(value: ContactFeedbackTopic) {
    form.topic = value;
    closeTopicSelect();
}

function handleDocumentClick(event: MouseEvent) {
    if (!topicSelectRef.value?.contains(event.target as Node)) {
        closeTopicSelect();
    }
}

function handleTopicSelectKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        closeTopicSelect();
    }
}

onMounted(() => {
    document.addEventListener("click", handleDocumentClick);
});

onBeforeUnmount(() => {
    document.removeEventListener("click", handleDocumentClick);
});
</script>

<template>
    <section class="section contact-form-section">
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="contact-form-wrapper fade-in visible">
                <div class="contact-form-card-full">
                    <form
                        id="contactFeedbackForm"
                        class="contact-feedback-form"
                        method="POST"
                        enctype="multipart/form-data"
                        @submit.prevent="submitForm"
                    >
                        <div class="form-row">
                            <div class="form-group">
                                <label
                                    for="cf-name"
                                    class="form-label"
                                >
                                    {{ content.fields.name.label }}
                                </label>

                                <input
                                    id="cf-name"
                                    v-model="form.fullName"
                                    type="text"
                                    name="name"
                                    class="form-input"
                                    :placeholder="content.fields.name.placeholder"
                                    required
                                />

                                <p
                                    v-if="errors.fullName"
                                    class="contact-form-error"
                                >
                                    {{ errors.fullName }}
                                </p>
                            </div>

                            <div class="form-group">
                                <label
                                    for="cf-email"
                                    class="form-label"
                                >
                                    {{ content.fields.email.label }}
                                </label>

                                <input
                                    id="cf-email"
                                    v-model="form.email"
                                    type="email"
                                    name="email"
                                    class="form-input"
                                    :placeholder="content.fields.email.placeholder"
                                    required
                                />

                                <p
                                    v-if="errors.email"
                                    class="contact-form-error"
                                >
                                    {{ errors.email }}
                                </p>
                            </div>
                        </div>

                        <div class="form-row contact-form-extra-row">
                            <div class="form-group">
                                <label
                                    for="cf-topic"
                                    class="form-label"
                                >
                                    {{ content.fields.topic.label }}
                                </label>

                                <div
                                    ref="topicSelectRef"
                                    class="custom-select custom-select--overlay contact-topic-select"
                                    :class="{ 'is-open': isTopicSelectOpen }"
                                    @keydown="handleTopicSelectKeydown"
                                >
                                    <button
                                        id="cf-topic"
                                        class="custom-select-trigger contact-topic-select-trigger"
                                        type="button"
                                        aria-haspopup="listbox"
                                        :aria-expanded="isTopicSelectOpen"
                                        :aria-controls="topicSelectId"
                                        @click.stop="toggleTopicSelect"
                                    >
                                        <span class="contact-topic-select-icon">
                                            <i class="fas fa-comments"></i>
                                        </span>

                                        <span class="custom-select-trigger-text">
                                            {{ selectedTopicLabel }}
                                        </span>

                                        <span class="custom-select-chevron">
                                            <i class="fas fa-chevron-down"></i>
                                        </span>
                                    </button>

                                    <div
                                        :id="topicSelectId"
                                        class="custom-select-dropdown contact-topic-select-dropdown"
                                        role="listbox"
                                    >
                                        <button
                                            v-for="topic in content.topics"
                                            :key="topic.value"
                                            class="custom-select-option contact-topic-select-option"
                                            :class="{ 'is-selected': form.topic === topic.value }"
                                            type="button"
                                            role="option"
                                            :aria-selected="form.topic === topic.value"
                                            @click="selectTopic(topic.value)"
                                        >
                                            {{ topic.label }}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <label
                                    for="cf-subject"
                                    class="form-label"
                                >
                                    {{ content.fields.subject.label }}
                                </label>

                                <input
                                    id="cf-subject"
                                    v-model="form.subject"
                                    type="text"
                                    name="subject"
                                    class="form-input"
                                    :placeholder="content.fields.subject.placeholder"
                                />
                            </div>
                        </div>

                        <div class="form-row contact-form-extra-row">
                            <div class="form-group">
                                <label
                                    for="cf-phone"
                                    class="form-label"
                                >
                                    {{ content.fields.phone.label }}
                                </label>

                                <input
                                    id="cf-phone"
                                    v-model="form.phone"
                                    type="tel"
                                    name="phone"
                                    class="form-input"
                                    :placeholder="content.fields.phone.placeholder"
                                />
                            </div>

                            <div class="form-group">
                                <label
                                    for="cf-organization"
                                    class="form-label"
                                >
                                    {{ content.fields.organization.label }}
                                </label>

                                <input
                                    id="cf-organization"
                                    v-model="form.organizationName"
                                    type="text"
                                    name="organization_name"
                                    class="form-input"
                                    :placeholder="content.fields.organization.placeholder"
                                />
                            </div>
                        </div>

                        <div class="form-group">
                            <label
                                for="cf-message"
                                class="form-label"
                            >
                                {{ content.fields.message.label }}
                            </label>

                            <textarea
                                id="cf-message"
                                v-model="form.message"
                                name="message"
                                class="form-textarea"
                                :placeholder="content.fields.message.placeholder"
                                required
                            ></textarea>

                            <p
                                v-if="errors.message"
                                class="contact-form-error"
                            >
                                {{ errors.message }}
                            </p>
                        </div>

                        <div class="form-group">
                            <label
                                for="cf-attachments"
                                class="form-label"
                            >
                                {{ content.fields.files.label }}
                            </label>

                            <div class="file-upload-wrapper">
                                <input
                                    id="cf-attachments"
                                    type="file"
                                    name="attachments[]"
                                    class="form-file"
                                    multiple
                                    accept="image/*,.pdf,.doc,.docx"
                                    @change="updateFiles"
                                />

                                <span class="file-upload-hint">
                                    {{ content.fields.files.hint }}
                                </span>

                                <span
                                    v-if="form.attachments.length"
                                    class="file-upload-hint"
                                >
                                    {{ t("contacts.selectedFiles", { count: form.attachments.length }) }}
                                </span>
                            </div>

                            <p
                                v-if="errors.attachments"
                                class="contact-form-error"
                            >
                                {{ errors.attachments }}
                            </p>
                        </div>

                        <div class="form-checkbox">
                            <input
                                id="cf-consent"
                                v-model="form.isPersonalDataConsent"
                                type="checkbox"
                                name="consent"
                                required
                            />

                            <label for="cf-consent">
                                {{ content.fields.consent }}
                            </label>
                        </div>

                        <p
                            v-if="errors.isPersonalDataConsent"
                            class="contact-form-error"
                        >
                            {{ errors.isPersonalDataConsent }}
                        </p>

                        <div
                            v-if="isSubmitted"
                            class="contact-form-success"
                        >
                            <i class="fas fa-check-circle"></i>
                            <span>{{ submitMessage || content.successText }}</span>
                        </div>

                        <p
                            v-if="errors.common"
                            class="contact-form-error contact-form-error--common"
                        >
                            {{ errors.common }}
                        </p>

                        <div class="contact-form-submit-row">
                            <button
                                type="submit"
                                class="form-submit-btn"
                                :disabled="isSubmitting"
                            >
                                <i class="fas fa-paper-plane"></i>
                                {{ isSubmitting ? content.submittingLabel : content.submitLabel }}
                            </button>

                            <button
                                v-if="isSubmitted"
                                type="button"
                                class="form-reset-btn"
                                @click="resetForm"
                            >
                                {{ content.resetLabel }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

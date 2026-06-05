<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import { formatRussianPhone } from "@/modules/auth/composables/usePhoneMask";
import type {
    ContactFeedbackContent,
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
    ContactFeedbackTopic,
} from "@/modules/public/types/contact.types";

interface Props {
    content: ContactFeedbackContent;
    form: ContactFeedbackFormState;
    errors: ContactFeedbackFormErrors;
}

const props = defineProps<Props>();

function selectTopic(value: string): void {
    props.form.topic = value as ContactFeedbackTopic;
}

function updatePhone(value: string): void {
    props.form.phone = formatRussianPhone(value);
}
</script>

<template>
    <div class="contact-feedback-details-fields">
        <div class="form-row">
            <div class="form-group">
                <label for="cf-name" class="form-label">{{ content.fields.name.label }}</label>
                <input
                    id="cf-name"
                    v-model="form.fullName"
                    type="text"
                    name="name"
                    class="form-input"
                    :placeholder="content.fields.name.placeholder"
                    required
                />
                <p v-if="errors.fullName" class="contact-form-error">{{ errors.fullName }}</p>
            </div>

            <div class="form-group">
                <label for="cf-email" class="form-label">{{ content.fields.email.label }}</label>
                <input
                    id="cf-email"
                    v-model="form.email"
                    type="email"
                    name="email"
                    class="form-input"
                    :placeholder="content.fields.email.placeholder"
                    required
                />
                <p v-if="errors.email" class="contact-form-error">{{ errors.email }}</p>
            </div>
        </div>

        <div class="form-row contact-form-extra-row">
            <div class="form-group">
                <label for="cf-topic" class="form-label">{{ content.fields.topic.label }}</label>
                <BaseSelect
                    id="cf-topic"
                    class="contact-topic-select"
                    :model-value="form.topic"
                    :options="content.topics"
                    :placeholder="content.fields.topic.label"
                    :aria-label="content.fields.topic.label"
                    mode="overlay"
                    @update:model-value="selectTopic"
                />
            </div>

            <div class="form-group">
                <label for="cf-subject" class="form-label">{{ content.fields.subject.label }}</label>
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
                <label for="cf-phone" class="form-label">{{ content.fields.phone.label }}</label>
                <input
                    id="cf-phone"
                    :value="form.phone"
                    type="tel"
                    name="phone"
                    class="form-input"
                    inputmode="tel"
                    :placeholder="content.fields.phone.placeholder"
                    @input="updatePhone(($event.target as HTMLInputElement).value)"
                />
            </div>

            <div class="form-group">
                <label for="cf-organization" class="form-label">{{ content.fields.organization.label }}</label>
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
    </div>
</template>

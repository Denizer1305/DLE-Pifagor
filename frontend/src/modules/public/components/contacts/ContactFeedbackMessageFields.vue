<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";
import type {
    ContactFeedbackContent,
    ContactFeedbackFormErrors,
    ContactFeedbackFormState,
} from "@/modules/public/types/contact.types";

interface Props {
    content: ContactFeedbackContent;
    form: ContactFeedbackFormState;
    errors: ContactFeedbackFormErrors;
}

interface Emits {
    (event: "update-files", value: Event): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
const { t } = useI18n();
</script>

<template>
    <div class="contact-feedback-message-fields">
        <div class="form-group">
            <label for="cf-message" class="form-label">{{ content.fields.message.label }}</label>
            <textarea
                id="cf-message"
                v-model="form.message"
                name="message"
                class="form-textarea"
                :placeholder="content.fields.message.placeholder"
                required
            ></textarea>
            <p v-if="errors.message" class="contact-form-error">{{ errors.message }}</p>
        </div>

        <div class="form-group">
            <label for="cf-attachments" class="form-label">{{ content.fields.files.label }}</label>
            <div class="file-upload-wrapper">
                <input
                    id="cf-attachments"
                    type="file"
                    name="attachments[]"
                    class="form-file"
                    multiple
                    accept="image/*,.pdf,.doc,.docx"
                    @change="emit('update-files', $event)"
                />
                <span class="file-upload-hint">{{ content.fields.files.hint }}</span>
                <span v-if="form.attachments.length" class="file-upload-hint">
                    {{ t("contacts.selectedFiles", { count: form.attachments.length }) }}
                </span>
            </div>
            <p v-if="errors.attachments" class="contact-form-error">{{ errors.attachments }}</p>
        </div>

        <div class="form-checkbox">
            <input
                id="cf-consent"
                v-model="form.isPersonalDataConsent"
                type="checkbox"
                name="consent"
                required
            />
            <label for="cf-consent">{{ content.fields.consent }}</label>
        </div>

        <p v-if="errors.isPersonalDataConsent" class="contact-form-error">
            {{ errors.isPersonalDataConsent }}
        </p>
    </div>
</template>

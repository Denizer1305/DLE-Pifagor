<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import ContactFeedbackDetailsFields from "@/modules/public/components/contacts/ContactFeedbackDetailsFields.vue";
import ContactFeedbackMessageFields from "@/modules/public/components/contacts/ContactFeedbackMessageFields.vue";
import { useContactFeedbackForm } from "@/modules/public/composables/useContactFeedbackForm";
import type { ContactFeedbackContent } from "@/modules/public/types/contact.types";

interface Props {
    content: ContactFeedbackContent;
}

defineProps<Props>();

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
                        <ContactFeedbackDetailsFields
                            :content="content"
                            :form="form"
                            :errors="errors"
                        />

                        <ContactFeedbackMessageFields
                            :content="content"
                            :form="form"
                            :errors="errors"
                            @update-files="updateFiles"
                        />

                        <div v-if="isSubmitted" class="contact-form-success">
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
                            <button type="submit" class="form-submit-btn" :disabled="isSubmitting">
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

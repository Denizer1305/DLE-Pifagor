<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import { formatRussianPhone } from "@/modules/auth/composables/usePhoneMask";
import type {
    ProfileEditFormContent,
    ProfileEditFormErrors,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";

interface Props {
    form: ProfileEditFormState;
    errors: ProfileEditFormErrors;
    content: ProfileEditFormContent["contacts"];
}

const props = defineProps<Props>();

function handlePhoneInput(event: Event): void {
    const input = event.target as HTMLInputElement;

    props.form.phone = formatRussianPhone(input.value);
}
</script>

<template>
    <section class="profile-edit-section profile-edit-section-contacts fade-in visible">
        <div class="profile-edit-section-head">
            <div>
                <div class="profile-edit-section-topline">
                    <i :class="content.heading.icon"></i>
                    {{ content.heading.topline }}
                </div>
                <h2 class="profile-edit-section-title">{{ content.heading.title }}</h2>
                <p class="profile-edit-section-text">{{ content.heading.text }}</p>
            </div>
        </div>

        <div class="profile-edit-card">
            <div class="profile-edit-grid profile-edit-grid-2">
                <div class="profile-edit-field">
                    <label for="profile-email">{{ content.labels.email }}</label>
                    <input id="profile-email" v-model="form.email" type="email" disabled />
                    <span class="profile-edit-field-status is-success">
                        <i class="fas fa-check-circle"></i>
                        {{ content.emailStatus }}
                    </span>
                </div>
                <div class="profile-edit-field">
                    <label for="profile-phone">{{ content.labels.phone }}</label>
                    <input id="profile-phone" v-model="form.phone" type="tel" inputmode="tel" :placeholder="content.phonePlaceholder" @input="handlePhoneInput" />
                    <span v-if="errors.phone" class="profile-edit-field-status">{{ errors.phone }}</span>
                </div>
                <div class="profile-edit-field">
                    <label for="profile-backup-email">{{ content.labels.backupEmail }}</label>
                    <input id="profile-backup-email" v-model="form.backupEmail" type="email" :placeholder="content.backupEmailPlaceholder" />
                    <span v-if="errors.backupEmail" class="profile-edit-field-status">{{ errors.backupEmail }}</span>
                </div>
                <div class="profile-edit-field">
                    <label for="profile-vk">{{ content.labels.vkUrl }}</label>
                    <input id="profile-vk" v-model="form.vkUrl" type="url" />
                </div>
                <div class="profile-edit-field">
                    <label for="profile-max">{{ content.labels.maxUrl }}</label>
                    <input id="profile-max" v-model="form.maxUrl" type="text" />
                </div>
                <div class="profile-edit-field">
                    <label for="profile-contact-method">{{ content.labels.preferredContactMethod }}</label>
                    <BaseSelect id="profile-contact-method" v-model="form.preferredContactMethod" :options="content.contactMethodOptions" :aria-label="content.contactMethodAriaLabel" />
                </div>
            </div>
        </div>
    </section>
</template>

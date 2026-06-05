<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import ProfileCitySelect from "@/modules/profile/components/ProfileCitySelect.vue";
import type {
    ProfileCitySuggestion,
    ProfileEditFormContent,
    ProfileEditFormErrors,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";

interface Props {
    form: ProfileEditFormState;
    errors: ProfileEditFormErrors;
    content: ProfileEditFormContent["identity"];
    citySuggestions: ProfileCitySuggestion[];
    isCitySuggestionsLoading?: boolean;
}

interface Emits {
    (event: "search-city", value: string): void;
    (event: "select-city", suggestion: ProfileCitySuggestion): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="profile-edit-section profile-edit-section-identity fade-in visible">
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
            <div class="profile-edit-grid profile-edit-grid-3">
                <div class="profile-edit-field">
                    <label for="profile-last-name">{{ content.labels.lastName }}</label>
                    <input id="profile-last-name" v-model="form.lastName" type="text" />
                    <span v-if="errors.lastName" class="profile-edit-field-status">{{ errors.lastName }}</span>
                </div>
                <div class="profile-edit-field">
                    <label for="profile-first-name">{{ content.labels.firstName }}</label>
                    <input id="profile-first-name" v-model="form.firstName" type="text" />
                    <span v-if="errors.firstName" class="profile-edit-field-status">{{ errors.firstName }}</span>
                </div>
                <div class="profile-edit-field">
                    <label for="profile-middle-name">{{ content.labels.middleName }}</label>
                    <input id="profile-middle-name" v-model="form.middleName" type="text" />
                </div>
                <div class="profile-edit-field">
                    <label for="profile-birth-date">{{ content.labels.birthDate }}</label>
                    <input id="profile-birth-date" v-model="form.birthDate" type="date" />
                </div>
                <div class="profile-edit-field">
                    <label for="profile-gender">{{ content.labels.gender }}</label>
                    <BaseSelect id="profile-gender" v-model="form.gender" :options="content.genderOptions" :aria-label="content.genderAriaLabel" />
                </div>
                <div class="profile-edit-field">
                    <label for="profile-city">{{ content.labels.city }}</label>
                    <ProfileCitySelect
                        v-model="form.city"
                        :suggestions="citySuggestions"
                        :is-loading="isCitySuggestionsLoading"
                        @search="emit('search-city', $event)"
                        @select="emit('select-city', $event)"
                    />
                </div>
                <div class="profile-edit-field profile-edit-field-full">
                    <label for="profile-about">{{ content.labels.about }}</label>
                    <textarea id="profile-about" v-model="form.about" :placeholder="content.aboutPlaceholder"></textarea>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import type {
    ProfileEditFormContent,
    ProfileEditFormState,
} from "@/modules/profile/types/profile-edit.types";

interface Props {
    form: ProfileEditFormState;
    content: ProfileEditFormContent["display"];
}

defineProps<Props>();
</script>

<template>
    <section class="profile-edit-section profile-edit-section-display fade-in visible">
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
            <div class="profile-edit-toggle-list">
                <label
                    v-for="toggle in content.toggles"
                    :key="toggle.key"
                    class="profile-edit-toggle"
                >
                    <input v-model="form[toggle.key]" type="checkbox" />
                    <span class="profile-edit-toggle-ui"></span>
                    <span class="profile-edit-toggle-copy">
                        <strong>{{ toggle.label }}</strong>
                        <span>{{ toggle.text }}</span>
                    </span>
                </label>
            </div>
        </div>
    </section>
</template>

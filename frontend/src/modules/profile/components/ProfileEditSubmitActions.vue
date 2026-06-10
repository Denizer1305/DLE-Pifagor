<script setup lang="ts">
import { RouterLink } from "vue-router";

import type { ProfileEditSubmitContent } from "@/modules/profile/types/profile-edit.types";

interface Props {
    content: ProfileEditSubmitContent;
    isSubmitting: boolean;
}

defineProps<Props>();
</script>

<template>
    <section class="profile-edit-section profile-edit-section-submit fade-in visible">
        <div class="profile-edit-actions-card">
            <div>
                <strong>{{ content.title }}</strong>
                <span>{{ content.text }}</span>
            </div>

            <div class="profile-edit-actions">
                <RouterLink
                    v-if="content.cancelAction.to"
                    class="profile-edit-secondary-btn"
                    :to="content.cancelAction.to"
                >
                    {{ content.cancelAction.label }}
                </RouterLink>

                <button
                    type="submit"
                    class="profile-edit-main-btn"
                    :disabled="isSubmitting"
                >
                    <i :class="content.submitAction.icon"></i>
                    {{ isSubmitting ? content.submitAction.pendingLabel : content.submitAction.label }}
                </button>
            </div>
        </div>
    </section>
</template>

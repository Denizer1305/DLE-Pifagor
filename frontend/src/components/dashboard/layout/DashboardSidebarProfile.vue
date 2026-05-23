<script setup lang="ts">
import type { DashboardUserProfile } from "@/components/dashboard/types/dashboard.types";

interface Props {
    profile: DashboardUserProfile;
}

defineProps<Props>();
</script>

<template>
    <div class="sidebar-profile">
        <div class="sidebar-profile-avatar">
            <img
                v-if="profile.avatarUrl"
                :src="profile.avatarUrl"
                :alt="profile.avatarAlt"
            />

            <span v-else>
                {{ profile.fullName.slice(0, 1).toUpperCase() }}
            </span>
        </div>

        <div>
            <span class="sidebar-profile-name">
                {{ profile.fullName }}
            </span>

            <span class="sidebar-profile-role">
                {{ profile.roleLabel }}
            </span>
        </div>
    </div>
</template>

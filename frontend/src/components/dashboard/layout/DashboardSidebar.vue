<script setup lang="ts">
import { RouterLink, useRoute } from "vue-router";

import type {
    DashboardBrand,
    DashboardNavigationItem,
    DashboardSidebarExtraCard,
    DashboardUserProfile,
} from "@/components/dashboard/types/dashboard.types";

interface Props {
    brand: DashboardBrand;
    profile: DashboardUserProfile;
    navigation: DashboardNavigationItem[];
    extraCard?: DashboardSidebarExtraCard;
    isOpen?: boolean;
}

const props = defineProps<Props>();
const route = useRoute();

function isActive(item: DashboardNavigationItem): boolean {
    if (typeof item.to === "string") {
        return item.exact
            ? route.path === item.to
            : route.path.startsWith(item.to);
    }

    if ("name" in item.to && item.to.name) {
        return route.name === item.to.name;
    }

    if ("path" in item.to && item.to.path) {
        return item.exact
            ? route.path === item.to.path
            : route.path.startsWith(item.to.path);
    }

    return false;
}

function getExtraCardClass(): string {
    if (!props.extraCard) {
        return "";
    }

    if (props.extraCard.variant === "ai") {
        return "sidebar-ai";
    }

    if (props.extraCard.variant === "student") {
        return "sidebar-student-card";
    }

    return "sidebar-extra-card";
}
</script>

<template>
    <aside
        class="dashboard-sidebar"
        :class="{ 'is-open': isOpen }"
    >
        <div class="sidebar-card">
            <RouterLink
                class="sidebar-brand"
                :to="{ name: 'home' }"
            >
                <img
                    :src="brand.logo"
                    :alt="brand.title"
                />

                <div class="sidebar-brand-text">
                    <strong>{{ brand.title }}</strong>
                    <span>{{ brand.subtitle }}</span>
                </div>
            </RouterLink>

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

            <nav class="sidebar-nav">
                <RouterLink
                    v-for="item in navigation"
                    :key="item.key"
                    class="sidebar-nav-link"
                    :class="{ 'is-active': isActive(item) }"
                    :to="item.to"
                >
                    <span class="sidebar-nav-icon">
                        <i :class="item.icon"></i>
                    </span>

                    <span class="sidebar-nav-copy">
                        <strong>{{ item.label }}</strong>
                        <span>{{ item.description }}</span>
                    </span>

                    <span
                        v-if="item.badge !== undefined && item.badge !== null"
                        class="sidebar-nav-badge"
                    >
                        {{ item.badge }}
                    </span>
                </RouterLink>
            </nav>

            <div
                v-if="extraCard"
                :class="getExtraCardClass()"
            >
                <div
                    v-if="extraCard.variant === 'ai'"
                    class="sidebar-ai-top"
                >
                    <div class="sidebar-ai-mark">
                        <img
                            v-if="extraCard.image"
                            :src="extraCard.image.src"
                            :alt="extraCard.image.alt"
                        />

                        <i
                            v-else-if="extraCard.icon"
                            :class="extraCard.icon"
                        ></i>
                    </div>

                    <div>
                        <strong>{{ extraCard.title }}</strong>
                        <span>{{ extraCard.subtitle }}</span>
                    </div>
                </div>

                <div
                    v-else-if="extraCard.variant === 'student'"
                    class="sidebar-student-card-top"
                >
                    <div class="sidebar-student-card-icon">
                        <i :class="extraCard.icon"></i>
                    </div>

                    <div>
                        <strong>{{ extraCard.title }}</strong>
                        <span>{{ extraCard.subtitle }}</span>
                    </div>
                </div>

                <div
                    v-else
                    class="sidebar-extra-card-top"
                >
                    <div class="sidebar-extra-card-icon">
                        <i :class="extraCard.icon"></i>
                    </div>

                    <div>
                        <strong>{{ extraCard.title }}</strong>
                        <span>{{ extraCard.subtitle }}</span>
                    </div>
                </div>

                <p>
                    {{ extraCard.text }}
                </p>

                <RouterLink
                    v-if="extraCard.action.to"
                    class="sidebar-ai-btn"
                    :class="{ 'sidebar-student-card-btn': extraCard.variant === 'student' }"
                    :to="extraCard.action.to"
                >
                    <i :class="extraCard.action.icon"></i>
                    {{ extraCard.action.label }}
                </RouterLink>

                <a
                    v-else
                    class="sidebar-ai-btn"
                    :class="{ 'sidebar-student-card-btn': extraCard.variant === 'student' }"
                    :href="extraCard.action.href || '#'"
                >
                    <i :class="extraCard.action.icon"></i>
                    {{ extraCard.action.label }}
                </a>
            </div>
        </div>
    </aside>
</template>

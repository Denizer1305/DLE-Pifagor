<script setup lang="ts">
import { RouterLink } from "vue-router";

import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardPageNav from "@/components/dashboard/shared/DashboardPageNav.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";
import {
    adminUserOrderingOptions,
    adminUserStatusOptions,
    adminUsersNavActions,
    adminUsersNavItems,
    adminUsersPageContent,
} from "@/modules/admin/data/admin-users.data";
import type {
    AdminUsersFilters,
    AdminUsersListModel,
} from "@/modules/admin/types/admin-users.types";

interface Props {
    model: AdminUsersListModel;
    filters: AdminUsersFilters;
    isLoading: boolean;
    errorMessage: string;
    canGoPrevious: boolean;
    canGoNext: boolean;
}

interface Emits {
    (event: "reload"): void;
    (event: "search"): void;
    (event: "reset"): void;
    (event: "set-search", value: string): void;
    (event: "set-filter", key: "status" | "ordering", value: string): void;
    (event: "previous"): void;
    (event: "next"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="admin-users-page fade-in visible">
        <header class="admin-users-hero">
            <span class="dashboard-badge">
                <i class="fas fa-users"></i>
                {{ model.badge }}
            </span>
            <h1>{{ model.title }}</h1>
            <p>{{ model.text }}</p>
        </header>

        <DashboardPageNav
            :items="adminUsersNavItems"
            :actions="adminUsersNavActions"
            aria-label="Навигация по пользователям"
        />

        <div class="admin-users-summary">
            <article
                v-for="item in model.summary"
                :key="item.key"
            >
                <i :class="item.icon"></i>
                <span>{{ item.label }}</span>
                <strong>{{ item.value }}</strong>
            </article>
        </div>

        <form
            class="admin-users-filters"
            @submit.prevent="emit('search')"
        >
            <label class="admin-users-search">
                <i class="fas fa-magnifying-glass"></i>
                <input
                    :value="filters.search"
                    type="search"
                    :placeholder="adminUsersPageContent.searchPlaceholder"
                    @input="emit('set-search', ($event.target as HTMLInputElement).value)"
                />
            </label>

            <BaseSelect
                :model-value="filters.status"
                :options="adminUserStatusOptions"
                :aria-label="adminUsersPageContent.filters.status"
                @update:model-value="emit('set-filter', 'status', $event)"
            />

            <BaseSelect
                :model-value="filters.ordering"
                :options="adminUserOrderingOptions"
                :aria-label="adminUsersPageContent.filters.ordering"
                @update:model-value="emit('set-filter', 'ordering', $event)"
            />

            <button
                type="submit"
                class="dashboard-course-btn primary"
            >
                <i class="fas fa-filter"></i>
                {{ adminUsersPageContent.applyLabel }}
            </button>

            <button
                type="button"
                class="dashboard-course-btn"
                @click="emit('reset')"
            >
                {{ adminUsersPageContent.resetLabel }}
            </button>
        </form>

        <p
            v-if="errorMessage"
            class="admin-users-error"
        >
            {{ errorMessage }}
            <button
                type="button"
                @click="emit('reload')"
            >
                {{ adminUsersPageContent.retryLabel }}
            </button>
        </p>

        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="adminUsersPageContent.loadingText"
        />

        <div
            v-else-if="model.items.length"
            class="admin-users-table-wrap"
        >
            <table class="admin-users-table">
                <thead>
                    <tr>
                        <th>Пользователь</th>
                        <th>Роль</th>
                        <th>Статус</th>
                        <th>Обновлен</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="user in model.items"
                        :key="user.id"
                    >
                        <td data-label="Пользователь">
                            <strong>{{ user.fullName }}</strong>
                            <small>{{ user.email }} · {{ user.phone }}</small>
                        </td>
                        <td data-label="Роль">{{ user.roleLabel }}</td>
                        <td data-label="Статус">
                            <mark :class="`is-${user.statusTone}`">
                                {{ user.statusLabel }}
                            </mark>
                        </td>
                        <td data-label="Обновлен">{{ user.updatedAt }}</td>
                        <td data-label="Действия">
                            <span class="admin-users-actions">
                                <RouterLink :to="{ name: 'admin-user-detail', params: { id: user.id } }">
                                    {{ adminUsersPageContent.detailsLabel }}
                                </RouterLink>
                                <RouterLink :to="{ name: 'admin-user-edit', params: { id: user.id } }">
                                    {{ adminUsersPageContent.editLabel }}
                                </RouterLink>
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div
            v-else
            class="admin-users-empty"
        >
            <i class="fas fa-user-plus"></i>
            <strong>{{ model.emptyTitle }}</strong>
            <p>{{ model.emptyText }}</p>
        </div>

        <footer class="admin-users-pagination">
            <span>{{ model.totalLabel }}: {{ model.total }}</span>
            <strong>
                Страница {{ model.currentPage }} из {{ model.totalPages }}
            </strong>
            <div>
                <button
                    type="button"
                    :disabled="!canGoPrevious"
                    @click="emit('previous')"
                >
                    {{ adminUsersPageContent.previousLabel }}
                </button>
                <button
                    type="button"
                    :disabled="!canGoNext"
                    @click="emit('next')"
                >
                    {{ adminUsersPageContent.nextLabel }}
                </button>
            </div>
        </footer>
    </section>
</template>

<script setup lang="ts">
import DashboardPageNav from "@/components/dashboard/shared/DashboardPageNav.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";
import { adminUserDetailContent } from "@/modules/admin/data/admin-users.data";
import type {
    AdminUserDetailModel,
    AdminUserStatusAction,
} from "@/modules/admin/types/admin-users.types";

interface Props {
    user: AdminUserDetailModel | null;
    isLoading: boolean;
    updatingAction: AdminUserStatusAction | null;
    errorMessage: string;
}

interface Emits {
    (event: "reload"): void;
    (event: "status-action", action: AdminUserStatusAction): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="admin-user-detail fade-in visible">
        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="adminUserDetailContent.loadingText"
        />

        <DashboardStateView
            v-else-if="errorMessage"
            variant="error"
            :title="adminUserDetailContent.errorTitle"
            :text="errorMessage"
            :action-label="adminUserDetailContent.backLabel"
            action-icon="fas fa-rotate-right"
            @action="emit('reload')"
        />

        <template v-else-if="user">
            <header class="admin-user-card admin-user-detail-hero">
                <div>
                    <span class="dashboard-badge">
                        <i class="fas fa-id-card"></i>
                        {{ user.roleLabel }}
                    </span>
                    <h1>{{ user.title }}</h1>
                    <p>{{ user.subtitle }}</p>
                </div>

                <DashboardPageNav
                    class="admin-user-detail-nav"
                    :items="[
                        {
                            key: 'users',
                            label: adminUserDetailContent.backLabel,
                            icon: 'fas fa-arrow-left',
                            to: { name: 'admin-users' },
                        },
                    ]"
                    :actions="[
                        {
                            key: 'edit',
                            label: adminUserDetailContent.editLabel,
                            icon: 'fas fa-user-pen',
                            to: { name: 'admin-user-edit', params: { id: user.id } },
                        },
                    ]"
                    aria-label="Навигация карточки пользователя"
                />
            </header>

            <div class="admin-user-detail-grid">
                <article class="admin-user-card">
                    <h2>{{ adminUserDetailContent.mainTitle }}</h2>
                    <dl>
                        <template
                            v-for="field in user.fields"
                            :key="field.label"
                        >
                            <dt>{{ field.label }}</dt>
                            <dd>{{ field.value }}</dd>
                        </template>
                    </dl>
                </article>

                <article class="admin-user-card">
                    <h2>{{ adminUserDetailContent.rolesTitle }}</h2>
                    <dl v-if="user.roles.length">
                        <template
                            v-for="field in user.roles"
                            :key="field.label + field.value"
                        >
                            <dt>{{ field.label }}</dt>
                            <dd>{{ field.value }}</dd>
                        </template>
                    </dl>
                    <p v-else>Роли пока не назначены.</p>
                </article>

                <article class="admin-user-card admin-user-profile-card">
                    <h2>Профиль</h2>
                    <dl>
                        <template
                            v-for="field in user.profileFields"
                            :key="field.label"
                        >
                            <dt>{{ field.label }}</dt>
                            <dd>{{ field.value }}</dd>
                        </template>
                    </dl>
                </article>
            </div>

            <div class="admin-user-status-actions">
                <button
                    v-if="user.canBlock"
                    type="button"
                    :disabled="updatingAction === 'block'"
                    @click="emit('status-action', 'block')"
                >
                    {{ adminUserDetailContent.blockLabel }}
                </button>
                <button
                    v-if="user.canUnblock"
                    type="button"
                    :disabled="updatingAction === 'unblock'"
                    @click="emit('status-action', 'unblock')"
                >
                    {{ adminUserDetailContent.unblockLabel }}
                </button>
                <button
                    type="button"
                    :disabled="updatingAction === 'archive'"
                    @click="emit('status-action', 'archive')"
                >
                    {{ adminUserDetailContent.archiveLabel }}
                </button>
                <button
                    v-if="user.canRestore"
                    type="button"
                    :disabled="updatingAction === 'restore'"
                    @click="emit('status-action', 'restore')"
                >
                    {{ adminUserDetailContent.restoreLabel }}
                </button>
            </div>

            <article class="admin-user-card">
                <h2>{{ adminUserDetailContent.auditTitle }}</h2>
                <div
                    v-if="user.audit.length"
                    class="admin-user-audit"
                >
                    <p
                        v-for="event in user.audit"
                        :key="event.label + event.value"
                    >
                        <time>{{ event.label }}</time>
                        <span>{{ event.value }}</span>
                    </p>
                </div>
                <p v-else>{{ adminUserDetailContent.emptyAudit }}</p>
            </article>
        </template>
    </section>
</template>

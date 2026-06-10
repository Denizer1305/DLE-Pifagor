<script setup lang="ts">
import DashboardPageNav from "@/components/dashboard/shared/DashboardPageNav.vue";
import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";
import { adminUserEditContent } from "@/modules/admin/data/admin-users.data";
import type {
    AdminUserDetailModel,
    AdminUserEditForm,
} from "@/modules/admin/types/admin-users.types";

interface Props {
    user: AdminUserDetailModel | null;
    form: AdminUserEditForm;
    isLoading: boolean;
    isSaving: boolean;
    errorMessage: string;
    saveMessage: string;
}

interface Emits {
    (event: "reload"): void;
    (event: "submit"): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="admin-user-edit fade-in visible">
        <DashboardStateView
            v-if="isLoading"
            variant="loading"
            :text="adminUserEditContent.loadingText"
        />

        <DashboardStateView
            v-else-if="errorMessage && !user"
            variant="error"
            :title="adminUserEditContent.errorTitle"
            :text="errorMessage"
            :action-label="adminUserEditContent.backLabel"
            action-icon="fas fa-rotate-right"
            @action="emit('reload')"
        />

        <form
            v-else-if="user"
            class="admin-user-card admin-user-edit-form"
            @submit.prevent="emit('submit')"
        >
            <header>
                <span class="dashboard-badge">
                    <i class="fas fa-user-pen"></i>
                    {{ user.roleLabel }}
                </span>
                <h1>{{ adminUserEditContent.title }}</h1>
                <p>{{ adminUserEditContent.text }}</p>
            </header>

            <DashboardPageNav
                :items="[
                    {
                        key: 'detail',
                        label: adminUserEditContent.backLabel,
                        icon: 'fas fa-arrow-left',
                        to: { name: 'admin-user-detail', params: { id: user.id } },
                    },
                    {
                        key: 'users',
                        label: 'Все пользователи',
                        icon: 'fas fa-users',
                        to: { name: 'admin-users' },
                    },
                ]"
                aria-label="Навигация редактирования пользователя"
            />

            <div class="admin-user-edit-grid">
                <label>
                    <span>{{ adminUserEditContent.fields.lastName }}</span>
                    <input
                        v-model="form.lastName"
                        type="text"
                        required
                    />
                </label>
                <label>
                    <span>{{ adminUserEditContent.fields.firstName }}</span>
                    <input
                        v-model="form.firstName"
                        type="text"
                        required
                    />
                </label>
                <label>
                    <span>{{ adminUserEditContent.fields.middleName }}</span>
                    <input
                        v-model="form.middleName"
                        type="text"
                    />
                </label>
                <label>
                    <span>{{ adminUserEditContent.fields.birthDate }}</span>
                    <input
                        v-model="form.birthDate"
                        type="date"
                    />
                </label>
                <label>
                    <span>{{ adminUserEditContent.fields.email }}</span>
                    <input
                        v-model="form.email"
                        type="email"
                        required
                    />
                </label>
                <label>
                    <span>{{ adminUserEditContent.fields.backupEmail }}</span>
                    <input
                        v-model="form.backupEmail"
                        type="email"
                    />
                </label>
                <label>
                    <span>{{ adminUserEditContent.fields.phone }}</span>
                    <input
                        v-model="form.phone"
                        type="tel"
                        required
                    />
                </label>
                <label class="admin-user-edit-toggle admin-checkbox-field">
                    <input
                        v-model="form.isLoginAllowed"
                        type="checkbox"
                    />
                    <span class="admin-checkbox-box"></span>
                    <span>{{ adminUserEditContent.fields.isLoginAllowed }}</span>
                </label>
            </div>

            <label class="admin-user-edit-reason">
                <span>{{ adminUserEditContent.fields.reason }}</span>
                <textarea
                    v-model="form.reason"
                    rows="4"
                ></textarea>
            </label>

            <p
                v-if="errorMessage"
                class="admin-users-error"
            >
                {{ errorMessage }}
            </p>
            <p
                v-if="saveMessage"
                class="admin-users-success"
            >
                {{ saveMessage }}
            </p>

            <footer class="admin-user-edit-actions">
                <button
                    type="submit"
                    class="dashboard-course-btn primary"
                    :disabled="isSaving"
                >
                    {{ isSaving ? adminUserEditContent.savingLabel : adminUserEditContent.saveLabel }}
                </button>
            </footer>
        </form>
    </section>
</template>

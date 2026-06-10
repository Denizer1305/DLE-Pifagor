<script setup lang="ts">
import BaseSelect from "@/components/base/BaseSelect.vue";
import DashboardPageNav from "@/components/dashboard/shared/DashboardPageNav.vue";
import { adminUserCreateContent, adminUserCreateRoleOptions } from "@/modules/admin/data/admin-users.data";
import type { AdminUserCreateForm } from "@/modules/admin/types/admin-users.types";

interface Props {
    form: AdminUserCreateForm;
    isSaving: boolean;
    errorMessage: string;
    saveMessage: string;
}

interface Emits {
    (event: "submit"): void;
    (event: "phone-input", value: Event): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section class="admin-user-edit admin-user-create fade-in visible">
        <form
            class="admin-user-card admin-user-edit-form"
            @submit.prevent="emit('submit')"
        >
            <header>
                <span class="dashboard-badge">
                    <i class="fas fa-user-plus"></i>
                    {{ adminUserCreateContent.badge }}
                </span>
                <h1>{{ adminUserCreateContent.title }}</h1>
                <p>{{ adminUserCreateContent.text }}</p>
            </header>

            <DashboardPageNav
                :items="[
                    {
                        key: 'users',
                        label: adminUserCreateContent.backLabel,
                        icon: 'fas fa-arrow-left',
                        to: { name: 'admin-users' },
                    },
                ]"
                aria-label="Навигация создания пользователя"
            />

            <div class="admin-user-edit-grid">
                <label>
                    <span>{{ adminUserCreateContent.fields.lastName }}</span>
                    <input
                        v-model="form.lastName"
                        type="text"
                        autocomplete="family-name"
                        required
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.firstName }}</span>
                    <input
                        v-model="form.firstName"
                        type="text"
                        autocomplete="given-name"
                        required
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.middleName }}</span>
                    <input
                        v-model="form.middleName"
                        type="text"
                        autocomplete="additional-name"
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.birthDate }}</span>
                    <input
                        v-model="form.birthDate"
                        type="date"
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.email }}</span>
                    <input
                        v-model="form.email"
                        type="email"
                        autocomplete="email"
                        required
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.backupEmail }}</span>
                    <input
                        v-model="form.backupEmail"
                        type="email"
                        autocomplete="email"
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.phone }}</span>
                    <input
                        :value="form.phone"
                        type="tel"
                        autocomplete="tel"
                        required
                        @input="emit('phone-input', $event)"
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.password }}</span>
                    <input
                        v-model="form.password"
                        type="text"
                        autocomplete="new-password"
                        :placeholder="adminUserCreateContent.placeholders.password"
                    />
                </label>

                <label>
                    <span>{{ adminUserCreateContent.fields.roleCode }}</span>
                    <BaseSelect
                        v-model="form.roleCode"
                        :options="adminUserCreateRoleOptions"
                        :placeholder="adminUserCreateContent.placeholders.roleCode"
                        aria-label="Выбрать первичную роль пользователя"
                    />
                </label>

                <label class="admin-user-edit-toggle admin-checkbox-field">
                    <input
                        v-model="form.isLoginAllowed"
                        type="checkbox"
                    />
                    <span class="admin-checkbox-box"></span>
                    <span>{{ adminUserCreateContent.fields.isLoginAllowed }}</span>
                </label>

                <label class="admin-user-edit-toggle admin-checkbox-field">
                    <input
                        v-model="form.sendInvite"
                        type="checkbox"
                    />
                    <span class="admin-checkbox-box"></span>
                    <span>{{ adminUserCreateContent.fields.sendInvite }}</span>
                </label>
            </div>

            <label class="admin-user-edit-reason">
                <span>{{ adminUserCreateContent.fields.reason }}</span>
                <textarea
                    v-model="form.reason"
                    rows="4"
                    :placeholder="adminUserCreateContent.placeholders.reason"
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
                    <i class="fas fa-user-plus"></i>
                    {{ isSaving ? adminUserCreateContent.submittingLabel : adminUserCreateContent.submitLabel }}
                </button>
            </footer>
        </form>
    </section>
</template>

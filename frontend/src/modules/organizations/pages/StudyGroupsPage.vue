<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import StudyGroupCodeModal from "../components/study-groups/StudyGroupCodeModal.vue";
import StudyGroupDetailsPanel from "../components/study-groups/StudyGroupDetailsPanel.vue";
import StudyGroupForm from "../components/study-groups/StudyGroupForm.vue";
import StudyGroupListTable from "../components/study-groups/StudyGroupListTable.vue";
import { useOrganizationDictionaries, useStudyGroups } from "../composables";
import {
    STUDY_FORM_OPTIONS,
    STUDY_GROUP_STATUS_OPTIONS,
} from "../data";
import type {
    OrganizationTableActionKey,
    StudyGroupDto,
    StudyGroupId,
    StudyGroupListItemView,
} from "../types";

type FormMode = "create" | "edit";

const {
    codeForm,
    emptyState,
    errorMessage,
    fieldErrors,
    filters,
    form,
    hasItems,
    isActionLoading,
    isDetailsLoading,
    isLoading,
    isSubmitting,
    items,
    selectedDetails,
    selectedItem,
    tableConfig,
    viewItems,
    archiveItem,
    clearSelection,
    createItem,
    fillForm,
    loadDetails,
    loadItems,
    resetCodeForm,
    resetForm,
    restoreItem,
    saveJoinCode,
    selectItem,
    setSearch,
    submitSearch,
    updateItem,
} = useStudyGroups();

const {
    getDepartmentOptions,
    organizationOptions,
    reloadDictionaries,
} = useOrganizationDictionaries();

const isFormModalOpen = ref(false);
const codeItemId = ref<StudyGroupId | null>(null);
const formMode = ref<FormMode>("create");

const departmentOptions = computed(() => {
    return getDepartmentOptions(form.organizationId);
});

const hasActiveFilters = computed(() => {
    return Boolean(filters.search);
});

function openCodeModal(id: StudyGroupId): void {
    codeItemId.value = id;
    resetCodeForm();
}

function closeCodeModal(): void {
    codeItemId.value = null;
    resetCodeForm();
}

function updateFormModel(value: typeof form): void {
    Object.assign(form, value);
}

function openCreateForm(): void {
    formMode.value = "create";
    resetForm();
    isFormModalOpen.value = true;
}

async function openEditForm(id?: StudyGroupId): Promise<void> {
    formMode.value = "edit";

    if (id) {
        await selectAndWaitDetails(id);
    } else if (selectedItem.value) {
        fillForm(selectedItem.value);
    }

    isFormModalOpen.value = true;
}

function closeFormModal(): void {
    isFormModalOpen.value = false;
    resetForm();
}

async function submitForm(): Promise<void> {
    if (formMode.value === "create") {
        await createItem();
    } else if (selectedItem.value) {
        await updateItem(selectedItem.value.id);
    }

    if (!Object.keys(fieldErrors.value).length) {
        await reloadDictionaries();
        isFormModalOpen.value = false;
    }
}

async function selectAndWaitDetails(id: StudyGroupId): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item: StudyGroupDto) => {
        return item.id === id;
    });

    if (selectedItem.value) {
        fillForm(selectedItem.value);
        return;
    }

    if (localItem) {
        fillForm(localItem);
    }
}

function handleTableAction(payload: {
    actionKey: OrganizationTableActionKey;
    item: StudyGroupListItemView;
}): void {
    if (payload.actionKey === "details") {
        selectItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "archive") {
        void archiveItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "edit") {
        void openEditForm(payload.item.id);
        return;
    }

    if (payload.actionKey === "restore") {
        void restoreItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "setCode") {
        openCodeModal(payload.item.id);
    }
}

async function submitJoinCode(): Promise<void> {
    if (!codeItemId.value) {
        return;
    }

    await saveJoinCode(codeItemId.value);
    closeCodeModal();
}

function copyCode(value: string): void {
    void navigator.clipboard?.writeText(value);
}

onMounted(() => {
    void loadItems();
});
</script>

<template>
    <OrganizationWorkspace
        :search-value="filters.search"
        search-placeholder="Поиск по группе, коду или организации"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Найти"
        refresh-label="Обновить"
        create-label="Создать группу"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <StudyGroupListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка учебной группы"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные учебной группы..."
                />

                <StudyGroupDetailsPanel
                    v-else
                    :details="selectedDetails"
                    @edit="openEditForm()"
                    @close="clearSelection"
                />
            </OrganizationDetailsModal>

            <StudyGroupCodeModal
                :is-open="Boolean(codeItemId)"
                v-model="codeForm"
                title="Код вступления в группу"
                text="Оставьте поле пустым, чтобы backend сгенерировал код автоматически."
                submit-label="Сохранить код"
                cancel-label="Отмена"
                :is-submitting="isSubmitting || isActionLoading"
                @submit="submitJoinCode"
                @cancel="closeCodeModal"
                @close="closeCodeModal"
                @copy="copyCode"
            />
        </template>
    </OrganizationWorkspace>

    <OrganizationDetailsModal
        :is-open="isFormModalOpen"
        :title="formMode === 'create' ? 'Создание учебной группы' : 'Редактирование учебной группы'"
        @close="closeFormModal"
    >
        <StudyGroupForm
            :model-value="form"
            :organization-options="organizationOptions"
            :department-options="departmentOptions"
            :status-options="STUDY_GROUP_STATUS_OPTIONS"
            :study-form-options="STUDY_FORM_OPTIONS"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новая учебная группа' : 'Данные учебной группы'"
            text="Заполните организацию, период обучения и параметры группы."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отмена"
            :is-submitting="isSubmitting"
            @update:model-value="updateFormModel"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>
</template>

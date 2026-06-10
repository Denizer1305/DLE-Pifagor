<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import GroupCuratorDetailsPanel from "../components/group-curators/GroupCuratorDetailsPanel.vue";
import GroupCuratorForm from "../components/group-curators/GroupCuratorForm.vue";
import GroupCuratorListTable from "../components/group-curators/GroupCuratorListTable.vue";
import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import { useGroupCurators, useOrganizationDictionaries } from "../composables";
import type {
    GroupCuratorDto,
    GroupCuratorId,
    GroupCuratorListItemView,
    OrganizationTableActionKey,
} from "../types";

type FormMode = "create" | "edit";

const {
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
    clearSelection,
    createItem,
    deactivateItem,
    fillForm,
    loadDetails,
    loadItems,
    resetForm,
    restoreItem,
    selectItem,
    setPrimaryItem,
    setSearch,
    submitSearch,
    updateItem,
} = useGroupCurators();

const {
    getStudyGroupOptions,
    reloadDictionaries,
    teacherOptions,
} = useOrganizationDictionaries();

const isFormModalOpen = ref(false);
const formMode = ref<FormMode>("create");

const groupOptions = computed(() => {
    return getStudyGroupOptions(filters.organizationId, filters.departmentId);
});

const hasActiveFilters = computed(() => {
    return Boolean(filters.search);
});

function updateFormModel(value: typeof form): void {
    Object.assign(form, value);
}

function openCreateForm(): void {
    formMode.value = "create";
    resetForm();
    isFormModalOpen.value = true;
}

async function openEditForm(id?: GroupCuratorId): Promise<void> {
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

async function selectAndWaitDetails(id: GroupCuratorId): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item: GroupCuratorDto) => {
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
    item: GroupCuratorListItemView;
}): void {
    if (payload.actionKey === "details") {
        selectItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "setPrimary") {
        void setPrimaryItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "edit") {
        void openEditForm(payload.item.id);
        return;
    }

    if (payload.actionKey === "deactivate") {
        void deactivateItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "restore") {
        void restoreItem(payload.item.id);
    }
}

onMounted(() => {
    void loadItems();
});
</script>

<template>
    <OrganizationWorkspace
        :search-value="filters.search"
        search-placeholder="Поиск по куратору, группе или email"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Найти"
        refresh-label="Обновить"
        create-label="Назначить куратора"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <GroupCuratorListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка куратора группы"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные куратора..."
                />

                <GroupCuratorDetailsPanel
                    v-else
                    :details="selectedDetails"
                    @edit="openEditForm()"
                    @close="clearSelection"
                />
            </OrganizationDetailsModal>
        </template>
    </OrganizationWorkspace>

    <OrganizationDetailsModal
        :is-open="isFormModalOpen"
        :title="formMode === 'create' ? 'Назначение куратора' : 'Редактирование куратора'"
        @close="closeFormModal"
    >
        <GroupCuratorForm
            :model-value="form"
            :group-options="groupOptions"
            :teacher-options="teacherOptions"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новый куратор' : 'Данные куратора'"
            text="Выберите учебную группу и преподавателя-куратора."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отмена"
            :is-submitting="isSubmitting"
            @update:model-value="updateFormModel"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>
</template>

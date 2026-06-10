<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import OrganizationCodeModal from "../components/organizations/OrganizationCodeModal.vue";
import OrganizationDetailsPanel from "../components/organizations/OrganizationDetailsPanel.vue";
import OrganizationForm from "../components/organizations/OrganizationForm.vue";
import OrganizationListFilters from "../components/organizations/OrganizationListFilters.vue";
import OrganizationListTable from "../components/organizations/OrganizationListTable.vue";
import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import {
    useOrganizationCitySuggestions,
    useOrganizationDictionaries,
    useOrganizations,
} from "../composables";
import type {
    OrganizationFormMode,
    OrganizationListItemView,
    OrganizationTableActionKey,
} from "../types";

const {
    emptyState,
    errorMessage,
    filters,
    form,
    codeForm,
    fieldErrors,
    generatedTeacherCode,
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
    restoreItem,
    resetCodeForm,
    resetForm,
    saveTeacherCode,
    selectItem,
    setActiveFilter,
    setPublicFilter,
    setSearch,
    submitSearch,
    updateItem,
} = useOrganizations();

const { reloadDictionaries } = useOrganizationDictionaries();
const {
    citySuggestions,
    isCitySuggestionsLoading,
    clearCitySuggestions,
    searchCities,
} = useOrganizationCitySuggestions();

const isFormModalOpen = ref(false);
const isCodeModalOpen = ref(false);
const formMode = ref<OrganizationFormMode>("create");

const hasActiveFilters = computed(() => {
    return Boolean(
        filters.search
        || filters.isActive !== null
        || filters.isPublic !== null,
    );
});

function handleTableAction(payload: {
    actionKey: OrganizationTableActionKey;
    item: OrganizationListItemView;
}): void {
    if (payload.actionKey === "details") {
        selectItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "edit") {
        void openEditForm(payload.item.id);
        return;
    }

    if (payload.actionKey === "setCode") {
        void openCodeModal(payload.item.id);
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

function updateFormModel(value: typeof form): void {
    Object.assign(form, value);
}

function updateCodeFormModel(value: typeof codeForm): void {
    Object.assign(codeForm, value);
}

function openCreateForm(): void {
    formMode.value = "create";
    resetForm();
    isFormModalOpen.value = true;
}

async function openEditForm(id?: number): Promise<void> {
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
    clearCitySuggestions();
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

async function openCodeModal(id?: number): Promise<void> {
    resetCodeForm();

    if (id && selectedItem.value?.id !== id) {
        await selectAndWaitDetails(id);
    }

    isCodeModalOpen.value = true;
}

function closeCodeModal(): void {
    isCodeModalOpen.value = false;
    resetCodeForm();
}

async function submitCodeForm(): Promise<void> {
    if (!selectedItem.value) {
        return;
    }

    await saveTeacherCode(selectedItem.value.id);
    await reloadDictionaries();
}

async function selectAndWaitDetails(id: number): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item) => item.id === id);

    if (selectedItem.value) {
        fillForm(selectedItem.value);
        return;
    }

    if (localItem) {
        fillForm(localItem);
    }
}

async function copyCode(value: string): Promise<void> {
    await navigator.clipboard?.writeText(value);
}

onMounted(() => {
    void loadItems();
});
</script>

<template>
    <OrganizationWorkspace
        :search-value="filters.search"
        search-placeholder="Поиск по названию, коду или городу"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Фильтры"
        refresh-label="Обновить"
        create-label="Создать организацию"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <template #filters>
            <OrganizationListFilters
                :is-active="filters.isActive"
                :is-public="filters.isPublic"
                :has-active-filters="hasActiveFilters"
                @set-active="setActiveFilter"
                @set-public="setPublicFilter"
                @reset="() => {
                    setActiveFilter(null);
                    setPublicFilter(null);
                }"
            />
        </template>

        <OrganizationListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка организации"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные организации..."
                />

                <OrganizationDetailsPanel
                    v-else
                    :details="selectedDetails"
                    @code="openCodeModal()"
                    @edit="openEditForm()"
                    @close="clearSelection"
                />
            </OrganizationDetailsModal>
        </template>
    </OrganizationWorkspace>

    <OrganizationDetailsModal
        :is-open="isFormModalOpen"
        :title="formMode === 'create' ? 'Создание организации' : 'Редактирование организации'"
        @close="closeFormModal"
    >
        <OrganizationForm
            :model-value="form"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новая организация' : 'Данные организации'"
            text="Заполните профиль, контакты и параметры публичного отображения организации."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отменить"
            :is-submitting="isSubmitting"
            :city-suggestions="citySuggestions"
            :is-city-suggestions-loading="isCitySuggestionsLoading"
            @update:model-value="updateFormModel"
            @search-city="searchCities"
            @select-city="($event) => {
                form.city = $event.value;
                clearCitySuggestions();
            }"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>

    <OrganizationCodeModal
        :is-open="isCodeModalOpen"
        :model-value="codeForm"
        title="Код подключения"
        text="Создайте или обновите код, который используется для подключения преподавателей к организации."
        submit-label="Сохранить код"
        cancel-label="Закрыть"
        :is-submitting="isActionLoading"
        :generated-code="generatedTeacherCode"
        @update:model-value="updateCodeFormModel"
        @submit="submitCodeForm"
        @cancel="closeCodeModal"
        @close="closeCodeModal"
        @copy="copyCode"
    />
</template>

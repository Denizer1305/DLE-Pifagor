<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";

import type {
    PublicTeachersOrganization,
    PublicTeachersSubject,
} from "@/modules/public/types/public-teachers.types";

interface Props {
    organization: PublicTeachersOrganization | null;
    subjects: PublicTeachersSubject[];
    search: string;
    subject: string;
    isFallback: boolean;
    teachersCount: number;
    searchPlaceholder: string;
    subjectPlaceholder: string;
}

interface Emits {
    (event: "update:search", value: string): void;
    (event: "update:subject", value: string): void;
    (event: "reset"): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const subjectSelectRef = ref<HTMLElement | null>(null);
const isSubjectSelectOpen = ref(false);
const subjectSelectId = "teachers-subject-select";
const localSearch = ref(props.search);
let searchDebounceTimer: number | null = null;

const selectedSubjectLabel = computed(() => {
    const selectedSubject = props.subjects.find((item) => item.code === props.subject);

    return selectedSubject?.shortName || selectedSubject?.name || props.subjectPlaceholder;
});

const hasSelectedSubject = computed(() => Boolean(props.subject));

function closeSubjectSelect() {
    isSubjectSelectOpen.value = false;
}

function toggleSubjectSelect() {
    isSubjectSelectOpen.value = !isSubjectSelectOpen.value;
}

function selectSubject(value: string) {
    emit("update:subject", value);
    closeSubjectSelect();
}

function emitSearch(value: string) {
    if (searchDebounceTimer) {
        window.clearTimeout(searchDebounceTimer);
    }

    searchDebounceTimer = window.setTimeout(() => {
        emit("update:search", value);
        searchDebounceTimer = null;
    }, 220);
}

function handleSearchInput(event: Event) {
    const value = (event.target as HTMLInputElement).value;

    localSearch.value = value;
    emitSearch(value);
}

function handleDocumentClick(event: MouseEvent) {
    if (!subjectSelectRef.value?.contains(event.target as Node)) {
        closeSubjectSelect();
    }
}

function handleSelectKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        closeSubjectSelect();
    }
}

onMounted(() => {
    document.addEventListener("click", handleDocumentClick);
});

onBeforeUnmount(() => {
    document.removeEventListener("click", handleDocumentClick);

    if (searchDebounceTimer) {
        window.clearTimeout(searchDebounceTimer);
    }
});

watch(
    () => props.search,
    (value) => {
        if (value !== localSearch.value) {
            localSearch.value = value;
        }
    },
);
</script>

<template>
    <div class="teachers-organization-filter">
        <div class="teachers-organization-filter-head">
            <div class="teachers-organization-filter-main">
                <span class="teachers-organization-filter-label">
                    Образовательная организация
                </span>

                <strong
                    v-if="organization"
                    class="teachers-organization-name"
                >
                    {{ organization.shortName || organization.name }}
                </strong>

                <p class="teachers-organization-filter-hint">
                    <span v-if="isFallback">
                        Для гостей показываем преподавателей организации по умолчанию.
                    </span>

                    <span v-else>
                        Для вас показаны преподаватели вашей образовательной организации.
                    </span>
                </p>
            </div>

            <span class="teachers-current-count">
                {{ teachersCount }} преподавателей
            </span>
        </div>

        <div class="teachers-filter-controls">
            <label class="teachers-filter-field teachers-filter-field-search">
                <span>Поиск</span>

                <input
                    :value="localSearch"
                    type="search"
                    :placeholder="searchPlaceholder"
                    @input="handleSearchInput"
                />
            </label>

            <div class="teachers-filter-field">
                <span>Предмет</span>

                <div
                    ref="subjectSelectRef"
                    class="custom-select custom-select--overlay teachers-subject-select"
                    :class="{ 'is-open': isSubjectSelectOpen }"
                    @keydown="handleSelectKeydown"
                >
                    <button
                        class="custom-select-trigger teachers-subject-select-trigger"
                        :class="{ 'is-placeholder': !hasSelectedSubject }"
                        type="button"
                        aria-haspopup="listbox"
                        :aria-expanded="isSubjectSelectOpen"
                        :aria-controls="subjectSelectId"
                        @click.stop="toggleSubjectSelect"
                    >
                        <span class="teachers-subject-select-icon">
                            <i class="fas fa-book-open"></i>
                        </span>

                        <span class="custom-select-trigger-text">
                            {{ selectedSubjectLabel }}
                        </span>

                        <span class="custom-select-chevron">
                            <i class="fas fa-chevron-down"></i>
                        </span>
                    </button>

                    <div
                        :id="subjectSelectId"
                        class="custom-select-dropdown teachers-subject-select-dropdown"
                        role="listbox"
                    >
                        <button
                            class="custom-select-option teachers-subject-select-option"
                            :class="{ 'is-selected': !subject }"
                            type="button"
                            role="option"
                            :aria-selected="!subject"
                            @click="selectSubject('')"
                        >
                            {{ subjectPlaceholder }}
                        </button>

                        <button
                            v-for="item in subjects"
                            :key="item.code"
                            class="custom-select-option teachers-subject-select-option"
                            :class="{ 'is-selected': subject === item.code }"
                            type="button"
                            role="option"
                            :aria-selected="subject === item.code"
                            @click="selectSubject(item.code)"
                        >
                            {{ item.shortName || item.name }}
                        </button>
                    </div>
                </div>
            </div>

            <button
                class="teachers-filter-reset"
                type="button"
                @click="emit('reset')"
            >
                Сбросить
            </button>
        </div>
    </div>
</template>

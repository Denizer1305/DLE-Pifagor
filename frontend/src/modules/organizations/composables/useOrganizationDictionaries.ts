import { computed, onMounted } from "vue";
import { storeToRefs } from "pinia";

import { useOrganizationDictionariesStore } from "../stores";

export function useOrganizationDictionaries() {
    const dictionariesStore = useOrganizationDictionariesStore();

    const {
        dictionaries,
        errorMessage,
        isLoaded,
        isLoading,
    } = storeToRefs(dictionariesStore);

    const organizationOptions = computed(() => {
        return dictionariesStore.organizationOptions;
    });

    const subjectOptions = computed(() => {
        return dictionariesStore.subjectOptions;
    });

    const teacherOptions = computed(() => {
        return dictionariesStore.teacherOptions;
    });

    function getDepartmentOptions(organizationId: number | null) {
        return dictionariesStore
            .getDepartmentsByOrganization(organizationId)
            .map((department) => {
                return {
                    label: department.shortName || department.name,
                    value: department.id,
                    hint: department.code,
                };
            });
    }

    function getStudyGroupOptions(
        organizationId: number | null,
        departmentId: number | null,
    ) {
        const groups = departmentId
            ? dictionariesStore.getStudyGroupsByDepartment(departmentId)
            : dictionariesStore.getStudyGroupsByOrganization(organizationId);

        return groups.map((group) => {
            return {
                label: group.name,
                value: group.id,
                hint: group.code,
            };
        });
    }

    async function loadDictionaries(): Promise<void> {
        await dictionariesStore.load();
    }

    async function reloadDictionaries(): Promise<void> {
        await dictionariesStore.reload();
    }

    onMounted(() => {
        void loadDictionaries();
    });

    return {
        dictionaries,
        errorMessage,
        isLoaded,
        isLoading,
        organizationOptions,
        subjectOptions,
        teacherOptions,
        getDepartmentOptions,
        getStudyGroupOptions,
        loadDictionaries,
        reloadDictionaries,
    };
}

import { defineStore } from "pinia";

import { loadOrganizationDictionaries } from "../services";
import type {
    DepartmentDictionaryItem,
    OrganizationModuleDictionaries,
    StudyGroupDictionaryItem,
    SubjectDto,
    TeacherDictionaryItem,
} from "../types";

interface DictionaryOption {
    label: string;
    value: number;
    hint?: string;
}

interface OrganizationDictionariesState {
    dictionaries: OrganizationModuleDictionaries;
    isLoading: boolean;
    isLoaded: boolean;
    errorMessage: string;
}

function createEmptyDictionaries(): OrganizationModuleDictionaries {
    return {
        organizations: [],
        departments: [],
        studyGroups: [],
        subjects: [],
        teachers: [],
    };
}

export const useOrganizationDictionariesStore = defineStore(
    "organizationDictionaries",
    {
        state: (): OrganizationDictionariesState => ({
            dictionaries: createEmptyDictionaries(),
            isLoading: false,
            isLoaded: false,
            errorMessage: "",
        }),

        getters: {
            organizationOptions(state): DictionaryOption[] {
                return state.dictionaries.organizations.map((organization) => {
                    return {
                        label: organization.short_name || organization.name,
                        value: organization.id,
                        hint: organization.code,
                    };
                });
            },

            subjectOptions(state): DictionaryOption[] {
                return state.dictionaries.subjects.map((subject) => {
                    return {
                        label: subject.short_name || subject.name,
                        value: subject.id,
                        hint: subject.code,
                    };
                });
            },

            teacherOptions(state): DictionaryOption[] {
                return state.dictionaries.teachers.map((teacher) => {
                    return {
                        label: teacher.fullName,
                        value: teacher.id,
                        hint: [teacher.email, teacher.phone]
                            .filter(Boolean)
                            .join(" · "),
                    };
                });
            },
        },

        actions: {
            async load(force = false): Promise<void> {
                if (this.isLoaded && !force) {
                    return;
                }

                this.isLoading = true;
                this.errorMessage = "";

                try {
                    this.dictionaries = await loadOrganizationDictionaries();
                    this.isLoaded = true;
                } catch (error) {
                    this.errorMessage = getDictionaryErrorMessage(error);
                } finally {
                    this.isLoading = false;
                }
            },

            async reload(): Promise<void> {
                await this.load(true);
            },

            reset(): void {
                this.dictionaries = createEmptyDictionaries();
                this.isLoading = false;
                this.isLoaded = false;
                this.errorMessage = "";
            },

            getDepartmentsByOrganization(
                organizationId: number | null,
            ): DepartmentDictionaryItem[] {
                if (!organizationId) {
                    return this.dictionaries.departments;
                }

                return this.dictionaries.departments.filter((department) => {
                    return department.organizationId === organizationId;
                });
            },

            getStudyGroupsByDepartment(
                departmentId: number | null,
            ): StudyGroupDictionaryItem[] {
                if (!departmentId) {
                    return this.dictionaries.studyGroups;
                }

                return this.dictionaries.studyGroups.filter((group) => {
                    return group.departmentId === departmentId;
                });
            },

            getStudyGroupsByOrganization(
                organizationId: number | null,
            ): StudyGroupDictionaryItem[] {
                if (!organizationId) {
                    return this.dictionaries.studyGroups;
                }

                return this.dictionaries.studyGroups.filter((group) => {
                    return group.organizationId === organizationId;
                });
            },

            findSubject(subjectId: number | null): SubjectDto | null {
                if (!subjectId) {
                    return null;
                }

                return this.dictionaries.subjects.find((subject) => {
                    return subject.id === subjectId;
                }) ?? null;
            },

            findTeacher(teacherId: number | null): TeacherDictionaryItem | null {
                if (!teacherId) {
                    return null;
                }

                return this.dictionaries.teachers.find((teacher) => {
                    return teacher.id === teacherId;
                }) ?? null;
            },
        },
    },
);

function getDictionaryErrorMessage(error: unknown): string {
    if (error instanceof Error && error.message) {
        return error.message;
    }

    return "Не удалось загрузить справочники организаций.";
}
<script setup lang="ts">
import type { ProfileEditFormState } from "@/modules/profile/types/profile-edit.types";
import type { ProfileRoleCode } from "@/modules/profile/types/profile.types";

interface Props {
    roleCode: ProfileRoleCode;
    form: ProfileEditFormState;
}

defineProps<Props>();
</script>

<template>
    <section class="profile-edit-section profile-edit-section-role fade-in visible">
        <div class="profile-edit-section-head">
            <div>
                <div class="profile-edit-role-topline">
                    <i class="fas fa-user-shield"></i>
                    Ролевые данные
                </div>

                <h2 class="profile-edit-role-title">
                    Данные активной роли
                </h2>

                <p class="profile-edit-section-text">
                    Эти поля относятся к активной роли пользователя. Организация, группа, отделение и статус
                    изменяются только администратором или ответственным сотрудником.
                </p>
            </div>
        </div>

        <div class="profile-edit-role-block">
            <div
                v-if="roleCode === 'teacher' || roleCode === 'curator' || roleCode === 'methodist' || roleCode === 'organizer' || roleCode === 'mentor'"
                class="profile-edit-grid profile-edit-grid-2"
            >
                <div class="profile-edit-field">
                    <label for="profile-role-public-title">Публичный заголовок</label>
                    <input
                        id="profile-role-public-title"
                        v-model="form.roleProfile.public_title"
                        type="text"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-role-experience">Педагогический стаж</label>
                    <input
                        id="profile-role-experience"
                        v-model="form.roleProfile.experience_years"
                        type="number"
                        min="0"
                    />
                </div>

                <div class="profile-edit-field profile-edit-field-full">
                    <label for="profile-role-short-bio">Краткое описание</label>
                    <textarea
                        id="profile-role-short-bio"
                        v-model="form.roleProfile.short_bio"
                    ></textarea>
                </div>

                <div class="profile-edit-field profile-edit-field-full">
                    <label for="profile-role-education">Образование</label>
                    <textarea
                        id="profile-role-education"
                        v-model="form.roleProfile.education"
                    ></textarea>
                </div>

                <div class="profile-edit-field profile-edit-field-full">
                    <label for="profile-role-achievements">Профессиональные достижения</label>
                    <textarea
                        id="profile-role-achievements"
                        v-model="form.roleProfile.achievements"
                    ></textarea>
                </div>
            </div>

            <div
                v-else-if="roleCode === 'guardian'"
                class="profile-edit-grid profile-edit-grid-2"
            >
                <div class="profile-edit-field">
                    <label for="profile-role-occupation">Род деятельности</label>
                    <input
                        id="profile-role-occupation"
                        v-model="form.roleProfile.occupation"
                        type="text"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-role-work-place">Место работы</label>
                    <input
                        id="profile-role-work-place"
                        v-model="form.roleProfile.work_place"
                        type="text"
                    />
                </div>

                <div class="profile-edit-field">
                    <label for="profile-role-emergency-phone">Экстренный телефон</label>
                    <input
                        id="profile-role-emergency-phone"
                        v-model="form.roleProfile.emergency_contact_phone"
                        type="tel"
                    />
                </div>

                <div class="profile-edit-field profile-edit-field-full">
                    <label for="profile-role-notes">Заметки</label>
                    <textarea
                        id="profile-role-notes"
                        v-model="form.roleProfile.notes"
                    ></textarea>
                </div>
            </div>

            <div
                v-else
                class="profile-edit-helper"
            >
                Для этой роли пока нет редактируемых дополнительных полей.
            </div>
        </div>
    </section>
</template>

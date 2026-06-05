<script setup lang="ts">
import SettingsToggleRow from "@/modules/settings/components/SettingsToggleRow.vue";
import type { PrivacySettingsDto } from "@/modules/settings/types/settings.types";

interface Props {
    settings: PrivacySettingsDto;
    disabled?: boolean;
}

interface Emits {
    (event: "update", value: Partial<PrivacySettingsDto>): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();

function updateField(
    key: keyof PrivacySettingsDto,
    value: boolean,
): void {
    emit("update", {
        [key]: value,
    });
}
</script>

<template>
    <div class="private-settings-matrix">
        <SettingsToggleRow
            label="Показывать email"
            text="Email будет доступен в профиле согласно уровню видимости."
            :model-value="settings.show_email"
            :disabled="disabled"
            @update:model-value="updateField('show_email', $event)"
        />

        <SettingsToggleRow
            label="Показывать телефон"
            text="Телефон будет отображаться в контактных данных профиля."
            :model-value="settings.show_phone"
            :disabled="disabled"
            @update:model-value="updateField('show_phone', $event)"
        />

        <SettingsToggleRow
            label="Показывать город"
            text="Город будет отображаться в персональной карточке."
            :model-value="settings.show_city"
            :disabled="disabled"
            @update:model-value="updateField('show_city', $event)"
        />

        <SettingsToggleRow
            label="Показывать дату рождения"
            text="Дата рождения будет видна в профиле пользователя."
            :model-value="settings.show_birth_date"
            :disabled="disabled"
            @update:model-value="updateField('show_birth_date', $event)"
        />

        <SettingsToggleRow
            label="Показывать ролевой профиль"
            text="Пользователи смогут видеть ролевую информацию профиля."
            :model-value="settings.show_role_profile"
            :disabled="disabled"
            @update:model-value="updateField('show_role_profile', $event)"
        />

        <SettingsToggleRow
            label="Показывать достижения"
            text="Достижения и награды будут доступны в профиле."
            :model-value="settings.show_achievements"
            :disabled="disabled"
            @update:model-value="updateField('show_achievements', $event)"
        />

        <SettingsToggleRow
            label="Доступ преподавателей"
            text="Преподаватели смогут видеть разрешённые данные профиля."
            :model-value="settings.allow_teachers_access"
            :disabled="disabled"
            @update:model-value="updateField('allow_teachers_access', $event)"
        />

        <SettingsToggleRow
            label="Доступ студентов"
            text="Студенты смогут видеть разрешённые данные профиля."
            :model-value="settings.allow_students_access"
            :disabled="disabled"
            @update:model-value="updateField('allow_students_access', $event)"
        />

        <SettingsToggleRow
            label="Доступ родителей"
            text="Родители смогут видеть разрешённые данные профиля."
            :model-value="settings.allow_guardians_access"
            :disabled="disabled"
            @update:model-value="updateField('allow_guardians_access', $event)"
        />

        <SettingsToggleRow
            label="Доступ администраторов"
            text="Администраторы могут видеть данные, необходимые для сопровождения."
            :model-value="settings.allow_admins_access"
            :disabled="disabled"
            @update:model-value="updateField('allow_admins_access', $event)"
        />
    </div>
</template>
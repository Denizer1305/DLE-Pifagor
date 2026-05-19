<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";
import type { RegistrationRole } from "@/modules/auth/types/auth-form.types";

interface RoleOption {
    value: RegistrationRole;
    label: string;
}

interface Props {
    modelValue: RegistrationRole;
}

interface Emits {
    (event: "update:modelValue", value: RegistrationRole): void;
}

defineProps<Props>();

const emit = defineEmits<Emits>();
const { tr } = useI18n();

const roleOptions: RoleOption[] = [
    {
        value: "learner",
        label: "Учащийся",
    },
    {
        value: "teacher",
        label: "Преподаватель",
    },
    {
        value: "guardian",
        label: "Родитель",
    },
];

function updateRole(value: RegistrationRole): void {
    emit("update:modelValue", value);
}
</script>

<template>
    <div class="form-group full">
        <label class="form-label">{{ tr("Выберите роль") }}</label>

        <div class="role-switcher">
            <label
                v-for="role in roleOptions"
                :key="role.value"
                class="role-option"
            >
                <input
                    type="radio"
                    name="role"
                    :value="role.value"
                    :checked="modelValue === role.value"
                    @change="updateRole(role.value)"
                />
                <span>{{ tr(role.label) }}</span>
            </label>
        </div>
    </div>
</template>

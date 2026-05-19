<script setup lang="ts">
import { useI18n } from "@/composables/useI18n";
import type {
    RegisterFormErrors,
    RegisterFormState,
    RegistrationRole,
} from "@/modules/auth/types/auth-form.types";

interface Props {
    form: RegisterFormState;
    errors: RegisterFormErrors;
    role: RegistrationRole;
}

defineProps<Props>();
const { tr } = useI18n();
</script>

<template>
    <div class="form-grid">
        <div class="form-group">
            <label class="form-label" for="lastName">
                {{ tr("Фамилия") }}
            </label>

            <input
                id="lastName"
                v-model="form.lastName"
                class="form-input"
                :class="{ 'is-invalid': errors.lastName }"
                type="text"
                autocomplete="family-name"
                :placeholder="tr('Иванов')"
            />

            <p v-if="errors.lastName" class="form-error form-error--compact">
                {{ tr("Проверьте фамилию") }}
            </p>
        </div>

        <div class="form-group">
            <label class="form-label" for="firstName">
                {{ tr("Имя") }}
            </label>

            <input
                id="firstName"
                v-model="form.firstName"
                class="form-input"
                :class="{ 'is-invalid': errors.firstName }"
                type="text"
                autocomplete="given-name"
                :placeholder="tr('Иван')"
            />

            <p v-if="errors.firstName" class="form-error form-error--compact">
                {{ tr("Проверьте имя") }}
            </p>
        </div>
    </div>

    <div class="form-grid">
        <div class="form-group">
            <label class="form-label" for="middleName">
                {{ tr("Отчество") }}
            </label>

            <input
                id="middleName"
                v-model="form.middleName"
                class="form-input"
                type="text"
                autocomplete="additional-name"
                :placeholder="tr('Иванович')"
            />
        </div>

        <div class="form-group">
            <label class="form-label" for="birthDate">
                {{ tr("Дата рождения") }}
            </label>

            <input
                id="birthDate"
                v-model="form.birthDate"
                class="form-input"
                :class="{ 'is-invalid': errors.birthDate }"
                type="date"
                autocomplete="bday"
            />

            <p v-if="errors.birthDate" class="form-error form-error--compact">
                {{ tr("Проверьте дату рождения") }}
            </p>
        </div>
    </div>
</template>

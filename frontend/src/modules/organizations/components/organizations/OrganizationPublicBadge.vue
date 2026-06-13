<script setup lang="ts">
interface Props {
    isPublic: boolean;
    isDefaultPublic?: boolean;
}

withDefaults(defineProps<Props>(), {
    isDefaultPublic: false,
});
</script>

<template>
    <div class="org-table__meta">
        <span
            class="org-table__status"
            :class="
                isPublic
                    ? 'org-table__status--active'
                    : 'org-table__status--inactive'
            "
        >
            {{ isPublic ? "Публичная" : "Скрытая" }}
        </span>

        <span
            v-if="isDefaultPublic"
            class="org-table__status org-table__status--verified"
        >
            По умолчанию
        </span>
    </div>
</template>

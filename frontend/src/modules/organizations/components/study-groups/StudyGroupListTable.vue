<script setup lang="ts">
import OrganizationActionMenu from "../shared/OrganizationActionMenu.vue";
import OrganizationStatusBadge from "../shared/OrganizationStatusBadge.vue";

import type {
    OrganizationTableAction,
    OrganizationTableActionKey,
    OrganizationTableColumn,
    StudyGroupListItemView,
} from "../../types";

interface Props {
    items: StudyGroupListItemView[];
    columns: OrganizationTableColumn[];
    actions: OrganizationTableAction[];
    disabledActions?: Partial<Record<number, OrganizationTableActionKey[]>>;
}

interface Emits {
    (event: "select", item: StudyGroupListItemView): void;
    (
        event: "action",
        payload: {
            actionKey: OrganizationTableActionKey;
            item: StudyGroupListItemView;
        },
    ): void;
}

const props = withDefaults(defineProps<Props>(), {
    disabledActions: () => ({}),
});

defineEmits<Emits>();

function getDisabledActions(item: StudyGroupListItemView): OrganizationTableActionKey[] {
    return props.disabledActions[item.id] ?? [];
}
</script>

<template>
    <section class="org-table">
        <div class="org-table__scroll">
            <table class="org-table__table">
                <thead class="org-table__head">
                    <tr class="org-table__row">
                        <th
                            v-for="column in columns"
                            :key="column.key"
                            class="org-table__cell org-table__cell--head"
                            :class="{
                                'org-table__cell--actions': column.key === 'actions',
                                'org-table__cell--compact': column.width,
                            }"
                            :style="{ width: column.width }"
                        >
                            {{ column.label }}
                        </th>
                    </tr>
                </thead>

                <tbody class="org-table__body">
                    <tr
                        v-for="item in items"
                        :key="item.id"
                        class="org-table__row"
                    >
                        <td
                            class="org-table__cell"
                            data-label="Группа"
                        >
                            <button
                                class="org-table__entity"
                                type="button"
                                @click="$emit('select', item)"
                            >
                                <span class="org-table__avatar">
                                    {{ item.title.slice(0, 2).toUpperCase() }}
                                </span>

                                <span class="org-table__entity-content">
                                    <span class="org-table__title">
                                        {{ item.title }}
                                    </span>

                                    <span class="org-table__subtitle">
                                        {{ item.subtitle }}
                                    </span>

                                    <span class="org-table__meta">
                                        <span
                                            v-for="metaItem in item.meta"
                                            :key="metaItem"
                                            class="org-table__meta-item"
                                        >
                                            {{ metaItem }}
                                        </span>
                                    </span>
                                </span>
                            </button>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Отделение"
                        >
                            <span class="org-table__title">
                                {{ item.departmentTitle }}
                            </span>

                            <span class="org-table__subtitle">
                                {{ item.organizationTitle }}
                            </span>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Период"
                        >
                            <span class="org-table__title">
                                {{ item.admissionYear }} — {{ item.graduationYear }}
                            </span>

                            <span class="org-table__subtitle">
                                {{ item.courseNumber }}
                            </span>
                        </td>

                        <td
                            class="org-table__cell"
                            data-label="Статус"
                        >
                            <OrganizationStatusBadge :status="item.status" />
                        </td>

                        <td
                            class="org-table__cell org-table__cell--actions"
                            data-label="Действия"
                        >
                            <OrganizationActionMenu
                                :actions="actions"
                                :disabled-actions="getDisabledActions(item)"
                                @action="
                                    $emit('action', {
                                        actionKey: $event,
                                        item,
                                    })
                                "
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>
</template>
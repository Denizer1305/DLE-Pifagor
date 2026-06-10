import { mapApiListResponse } from "../mappers";
import type { ApiListResponse } from "../types";

export interface OrganizationListServiceResult<TDto, TView> {
    items: TDto[];
    viewItems: TView[];
    totalCount: number;
    hasNext: boolean;
    hasPrevious: boolean;
}

export function createListServiceResult<TDto, TView>(
    response: ApiListResponse<TDto>,
    mapper: (items: TDto[]) => TView[],
): OrganizationListServiceResult<TDto, TView> {
    const normalizedResponse = mapApiListResponse(response);

    return {
        items: normalizedResponse.items,
        viewItems: mapper(normalizedResponse.items),
        totalCount: normalizedResponse.totalCount,
        hasNext: normalizedResponse.hasNext,
        hasPrevious: normalizedResponse.hasPrevious,
    };
}
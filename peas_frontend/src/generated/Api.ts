/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/** HTTPValidationError */
export interface HTTPValidationError {
  /** Detail */
  detail?: ValidationError[];
}

/** Pagination[ProductResponse] */
export interface PaginationProductResponse {
  /** Page */
  page: number;
  /** Page Size */
  page_size: number;
  /** Pages */
  pages: number;
  /** Total */
  total: number;
  /** Items */
  items: ProductResponse[];
}

/** Pagination[RecipeResponse] */
export interface PaginationRecipeResponse {
  /** Page */
  page: number;
  /** Page Size */
  page_size: number;
  /** Pages */
  pages: number;
  /** Total */
  total: number;
  /** Items */
  items: RecipeResponse[];
}

/** ProductDetail */
export interface ProductDetail {
  /**
   * Id
   * The ID of the product
   */
  id: number;
  /**
   * Quantity
   * Quantity of the product
   * @min 1
   */
  quantity: number;
  /** Unit of measurement for the product, using standard units */
  unit: Unit;
}

/** ProductRequest */
export interface ProductRequest {
  /**
   * Name
   * The name of the product
   */
  name: string;
  /**
   * Proteins
   * Protein content in grams
   * @min 0
   * @max 100
   */
  proteins: number;
  /**
   * Fats
   * Fat content in grams
   * @min 0
   * @max 100
   */
  fats: number;
  /**
   * Carbohydrates
   * Carbohydrate content in grams
   * @min 0
   * @max 100
   */
  carbohydrates: number;
  /**
   * Sodium
   * Sodium content in grams per 100g
   * @min 0
   * @max 100
   */
  sodium: number;
}

/** ProductResponse */
export interface ProductResponse {
  /**
   * Id
   * The unique identifier of the product
   */
  id: number;
  /**
   * Name
   * The name of the product
   */
  name: string;
  /**
   * Proteins
   * Protein content in grams per 100g
   */
  proteins: number;
  /**
   * Fats
   * Fat content in grams per 100g
   */
  fats: number;
  /**
   * Carbohydrates
   * Carbohydrate content in grams per 100g
   */
  carbohydrates: number;
  /**
   * Sodium
   * Sodium content in grams per 100g
   */
  sodium: number;
  /**
   * Calories
   * Caloric content in kcal per 100g
   */
  calories: number;
}

/** RecipeProductResponse */
export interface RecipeProductResponse {
  /** The product that is part of the recipe */
  product: ProductResponse;
  /**
   * Quantity
   * Quantity of the product
   */
  quantity: number;
  /** Unit of measurement for the product */
  unit: Unit;
}

/** RecipeRequest */
export interface RecipeRequest {
  /**
   * Name
   * The name of the recipe
   */
  name: string;
  /**
   * Description
   * The description of the recipe
   */
  description: string;
  /**
   * Servings
   * The number of servings the recipe
   */
  servings: number;
  /**
   * Products
   * List of products with quantities and units that are part of the recipe
   */
  products: ProductDetail[];
}

/** RecipeResponse */
export interface RecipeResponse {
  /**
   * Id
   * The unique identifier of the recipe
   */
  id: number;
  /**
   * Name
   * The name of the recipe
   */
  name: string;
  /**
   * Description
   * The description of the recipe
   */
  description: string;
  /**
   * Servings
   * The number of servings the recipe
   */
  servings: number;
  /**
   * Products
   * List of products that are part of the recipe
   */
  products: RecipeProductResponse[];
}

/** Unit */
export enum Unit {
  Gram = "gram",
  Milliliter = "milliliter",
}

/** ValidationError */
export interface ValidationError {
  /** Location */
  loc: (string | number)[];
  /** Message */
  msg: string;
  /** Error Type */
  type: string;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, "body" | "method" | "query" | "path">;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter((key) => "undefined" !== typeof query[key]);
    return keys
      .map((key) => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key)))
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string") ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== "string" ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { "Content-Type": type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === "undefined" || body === null ? null : payloadFormatter(body),
    }).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title Peas API
 * @version 1.0.0
 *
 * API for interacting with the Peas application
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  api = {
    /**
     * No description
     *
     * @tags Products
     * @name SearchProductsApiV1ProductsSearchGet
     * @summary Search Products
     * @request GET:/api/v1/products/search
     */
    searchProductsApiV1ProductsSearchGet: (
      query: {
        /**
         * Name
         * Search term for product name
         */
        name: string;
        /**
         * Page
         * @min 1
         * @default 1
         */
        page?: number;
        /**
         * Size
         * @min 1
         * @max 100
         * @default 50
         */
        size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginationProductResponse, HTTPValidationError>({
        path: `/api/v1/products/search`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Products
     * @name GetAllProductsApiV1ProductsGet
     * @summary Get All Products
     * @request GET:/api/v1/products
     */
    getAllProductsApiV1ProductsGet: (
      query?: {
        /**
         * Page
         * @min 1
         * @default 1
         */
        page?: number;
        /**
         * Size
         * @min 1
         * @max 100
         * @default 50
         */
        size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginationProductResponse, HTTPValidationError>({
        path: `/api/v1/products`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Products
     * @name CreateProductApiV1ProductsPost
     * @summary Create Product
     * @request POST:/api/v1/products
     */
    createProductApiV1ProductsPost: (data: ProductRequest, params: RequestParams = {}) =>
      this.request<ProductResponse, HTTPValidationError>({
        path: `/api/v1/products`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Products
     * @name GetProductByIdApiV1ProductsProductIdGet
     * @summary Get Product By Id
     * @request GET:/api/v1/products/{product_id}
     */
    getProductByIdApiV1ProductsProductIdGet: (productId: string, params: RequestParams = {}) =>
      this.request<ProductResponse, HTTPValidationError>({
        path: `/api/v1/products/${productId}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Products
     * @name UpdateProductApiV1ProductsProductIdPut
     * @summary Update Product
     * @request PUT:/api/v1/products/{product_id}
     */
    updateProductApiV1ProductsProductIdPut: (productId: string, data: ProductRequest, params: RequestParams = {}) =>
      this.request<ProductResponse, HTTPValidationError>({
        path: `/api/v1/products/${productId}`,
        method: "PUT",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Products
     * @name DeleteProductApiV1ProductsProductIdDelete
     * @summary Delete Product
     * @request DELETE:/api/v1/products/{product_id}
     */
    deleteProductApiV1ProductsProductIdDelete: (productId: string, params: RequestParams = {}) =>
      this.request<void, HTTPValidationError>({
        path: `/api/v1/products/${productId}`,
        method: "DELETE",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Recipes
     * @name SearchRecipesApiV1RecipesSearchGet
     * @summary Search Recipes
     * @request GET:/api/v1/recipes/search
     */
    searchRecipesApiV1RecipesSearchGet: (
      query: {
        /**
         * Name
         * Search term for product name
         */
        name: string;
        /**
         * Page
         * @min 1
         * @default 1
         */
        page?: number;
        /**
         * Size
         * @min 1
         * @max 100
         * @default 50
         */
        size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginationRecipeResponse, HTTPValidationError>({
        path: `/api/v1/recipes/search`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Recipes
     * @name GetAllRecipesApiV1RecipesGet
     * @summary Get All Recipes
     * @request GET:/api/v1/recipes
     */
    getAllRecipesApiV1RecipesGet: (
      query?: {
        /**
         * Page
         * @min 1
         * @default 1
         */
        page?: number;
        /**
         * Size
         * @min 1
         * @max 100
         * @default 50
         */
        size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginationRecipeResponse, HTTPValidationError>({
        path: `/api/v1/recipes`,
        method: "GET",
        query: query,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Recipes
     * @name CreateRecipeApiV1RecipesPost
     * @summary Create Recipe
     * @request POST:/api/v1/recipes
     */
    createRecipeApiV1RecipesPost: (data: RecipeRequest, params: RequestParams = {}) =>
      this.request<RecipeResponse, HTTPValidationError>({
        path: `/api/v1/recipes`,
        method: "POST",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Recipes
     * @name GetRecipeByIdApiV1RecipesRecipeIdGet
     * @summary Get Recipe By Id
     * @request GET:/api/v1/recipes/{recipe_id}
     */
    getRecipeByIdApiV1RecipesRecipeIdGet: (recipeId: string, params: RequestParams = {}) =>
      this.request<RecipeResponse, HTTPValidationError>({
        path: `/api/v1/recipes/${recipeId}`,
        method: "GET",
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Recipes
     * @name UpdateRecipeApiV1RecipesRecipeIdPut
     * @summary Update Recipe
     * @request PUT:/api/v1/recipes/{recipe_id}
     */
    updateRecipeApiV1RecipesRecipeIdPut: (recipeId: string, data: RecipeRequest, params: RequestParams = {}) =>
      this.request<RecipeResponse, HTTPValidationError>({
        path: `/api/v1/recipes/${recipeId}`,
        method: "PUT",
        body: data,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags Recipes
     * @name DeleteRecipeApiV1RecipesRecipeIdDelete
     * @summary Delete Recipe
     * @request DELETE:/api/v1/recipes/{recipe_id}
     */
    deleteRecipeApiV1RecipesRecipeIdDelete: (recipeId: string, params: RequestParams = {}) =>
      this.request<void, HTTPValidationError>({
        path: `/api/v1/recipes/${recipeId}`,
        method: "DELETE",
        ...params,
      }),
  };
}

package com.backend.utils.minio;

import lombok.Data;

@Data
public class ObjectItem {
    private String objectName;
    private Long size;
}
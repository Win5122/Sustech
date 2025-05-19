package com.backend;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;


@SpringBootApplication(scanBasePackages = {"com.backend", "com.backend.user"})
@MapperScan(basePackages = {"com.backend.user.mapper"})
@EnableCaching
public class SoftwareApplication {
    public static void main(String[] args) {
        SpringApplication.run(SoftwareApplication.class, args);
    }
}

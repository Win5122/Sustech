package com.backend.user.service;

import com.backend.user.entity.Permission;
import com.baomidou.mybatisplus.extension.service.IService;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * <p>
 * 服务类
 * </p>
 *
 * @author mumu
 * @since 2023-10-15
 */
@Transactional
public interface PermissionService extends IService<Permission> {

    boolean insertPermission(String id, List<Integer> permission);

    boolean deletePermission(String id, List<Integer> permission);
}

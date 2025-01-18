package com.backend.user.entity.dto;

import com.backend.user.entity.Role;
import lombok.Data;
import lombok.ToString;

import java.util.List;

@Data
@ToString
public class UserInfoDTO {
    private String userId;

    private String userName;

    private String userImg;

    private String userMail;

    private String userMajor;

    private List<Role> userPermission;
}

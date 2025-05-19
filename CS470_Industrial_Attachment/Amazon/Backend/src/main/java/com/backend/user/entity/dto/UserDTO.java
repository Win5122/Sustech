package com.backend.user.entity.dto;

import com.backend.user.entity.Role;
import lombok.Data;
import lombok.ToString;

import java.io.Serial;
import java.io.Serializable;
import java.util.List;

@Data
@ToString
public class UserDTO implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;

    private String userId;

    private String userName;

    private String userPassword;

    private String userImg;

    private List<Role> userPermission;

    private String userMail;

    private String userMajor;
}

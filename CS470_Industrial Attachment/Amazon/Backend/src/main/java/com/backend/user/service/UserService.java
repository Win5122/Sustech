package com.backend.user.service;

import com.backend.user.entity.User;
import com.backend.user.entity.dto.UserDTO;
import com.backend.user.entity.dto.UserInfoDTO;
import com.backend.utils.AjaxJson;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;
import java.util.Map;

/**
 * <p>
 * 服务类
 * </p>
 *
 * @author mumu
 * @since 2023-09-22
 */
public interface UserService extends IService<User> {

    int setUserRank(String userid, String rank);

    int setUserScore(String userid, Float score);

    AjaxJson setUserMajor(String userid, String major);

    AjaxJson setUserMail(String userid, String mail);

    UserDTO getUser(String id);

    Map<String, Object> getUserMap(String id);

    AjaxJson changePassword(String userId, String password, String newpassword);

    List<User> selectList();

    boolean isUserIdExists(String userId);

    String getUserId(String userName);

    UserInfoDTO login(String userId);

    boolean isUserIdExists(String userId, String password);

    AjaxJson resetPassword(User user);

    AjaxJson resetPassword(String userid);

    AjaxJson resetPassword(String code, String password);

    AjaxJson getUserInformation(String userId);

    AjaxJson getUserSelfInformation(String userId);

    boolean isAdmin(String userId);

    boolean isBlack(String userId);

    Float countScore(String userId);

    User getUserById(String userId);

    List<User> getRank(String userMajor);

    List<Map<String, Object>> getAllScoreMap(String userId);
}

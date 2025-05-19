package com.backend.user.service.impl;

import com.backend.user.entity.Permission;
import com.backend.user.entity.Role;
import com.backend.user.entity.User;
import com.backend.user.entity.dto.UserDTO;
import com.backend.user.entity.dto.UserInfoDTO;
import com.backend.user.mapper.UserMapper;
import com.backend.user.service.UserService;
import com.backend.utils.AjaxJson;
import com.backend.utils.MyMailService;
import com.backend.utils.VerificationCodeGenerator;
import com.backend.utils.redis.RedisOptService;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.conditions.update.LambdaUpdateWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.github.yulichang.wrapper.MPJLambdaWrapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * <p>
 * 服务实现类
 * </p>
 *
 * @author mumu
 * @since 2023-09-22
 */
@Service
@Transactional
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
    private static Map<String, String> resetPasswordCode = new HashMap<>();
    @Autowired
    UserMapper mapper;
    @Autowired
    RedisOptService redisOptService;
    @Autowired
    VerificationCodeGenerator verificationCode;
    @Autowired
    MyMailService mailService;

    @Override
    public int setUserRank(String userid, String rank) {
        LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
        updateWrapper.eq(User::getUserId, userid)
                .set(User::getUserRank, rank);
        return mapper.update(null, updateWrapper);
    }

    @Override
    public int setUserScore(String userid, Float score) {
        LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
        updateWrapper.eq(User::getUserId, userid)
                .set(User::getUserScore, score);
        return mapper.update(null, updateWrapper);
    }

    @Override
    public AjaxJson setUserMajor(String userid, String major) {
        LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
        updateWrapper.eq(User::getUserId, userid)
                .set(User::getUserMajor, major);
        return 1 == mapper.update(null, updateWrapper) ? AjaxJson.getSuccess() : AjaxJson.getError("Error!");
    }

    @Override
    public AjaxJson setUserMail(String userid, String mail) {
        LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
        updateWrapper.eq(User::getUserId, userid)
                .set(User::getUserMail, mail);
        return 1 == mapper.update(null, updateWrapper) ? AjaxJson.getSuccess() : AjaxJson.getError("Error!");
    }


    @Override
    public UserDTO getUser(String userid) {
//        UserDTO ud = (UserDTO) redisOptService.get(userid);
//        if (ud != null)
//            return ud;
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .selectCollection(Role.class, UserDTO::getUserPermission)
                .leftJoin(Permission.class, Permission::getUserId, User::getUserId)
                .leftJoin(Role.class, Role::getRoleId, Permission::getRoleId)
                .eq(User::getUserId, userid);
//        ud = mapper.selectJoinOne(UserDTO.class, queryWrapper);
//        redisOptService.set(userid, ud);
//        return ud;
        return mapper.selectJoinOne(UserDTO.class, queryWrapper);
    }

    @Override
    public Map<String, Object> getUserMap(String userid) {
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .selectCollection(Role.class, UserDTO::getUserPermission)
                .leftJoin(Permission.class, Permission::getUserId, User::getUserId)
                .leftJoin(Role.class, Role::getRoleId, Permission::getRoleId)
                .eq(User::getUserId, userid);
        return mapper.selectJoinMap(queryWrapper);
    }

    @Override
    public AjaxJson changePassword(String userId, String password, String newpassword) {
        LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
        updateWrapper.eq(User::getUserId, userId)
                .eq(User::getUserPassword, password)
                .set(User::getUserPassword, newpassword);
        return 1 == mapper.update(null, updateWrapper) ? AjaxJson.getSuccess() : AjaxJson.getError("wrong password");

    }

    @Override
    public List<User> selectList() {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        return mapper.selectList(queryWrapper);
    }

    @Override
    public boolean isUserIdExists(String userId) {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("user_id", userId);
        return mapper.selectCount(queryWrapper) > 0;
    }

    @Override
    public String getUserId(String userName) {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("user_name", userName);
        return mapper.selectList(queryWrapper).get(0).getUserId();
    }

    @Override
    public UserInfoDTO login(String userId) {
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .selectCollection(Role.class, UserInfoDTO::getUserPermission)
                .leftJoin(Permission.class, Permission::getUserId, User::getUserId)
                .leftJoin(Role.class, Role::getRoleId, Permission::getRoleId)
                .eq(User::getUserId, userId);
        return mapper.selectJoinOne(UserInfoDTO.class, queryWrapper);
    }

    @Override
    public boolean isUserIdExists(String userId, String password) {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.eq("user_id", userId);
        queryWrapper.eq("user_password", password);
        return mapper.selectCount(queryWrapper) > 0;
    }

    /**
     * reset to a certain password
     *
     * @param user
     * @return
     */
    @Override
    public AjaxJson resetPassword(User user) {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.lambda().eq(user.getUserId() != null, User::getUserId, user.getUserId())
                .eq(user.getUserName() != null, User::getUserName, user.getUserName());
        switch (mapper.selectCount(queryWrapper)) {
            case 0:
                return AjaxJson.getError("no user found");
            case 1:
                LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
                updateWrapper.eq(user.getUserId() != null, User::getUserId, user.getUserId())
                        .eq(user.getUserName() != null, User::getUserName, user.getUserName());
                updateWrapper.set(User::getUserPassword, user.getUserPassword());
                return 1 == mapper.update(null, updateWrapper) ? AjaxJson.getSuccess() : AjaxJson.getError("error occurred");
            default:
                return AjaxJson.getError("too many users found, please give the userId");
        }
    }

    /**
     * send reset mail
     */
    @Override
    public AjaxJson resetPassword(String userid) {
        QueryWrapper<User> queryWrapper = new QueryWrapper<>();
        queryWrapper.lambda().eq(User::getUserId, userid);
        String toMail = mapper.selectOne(queryWrapper).getUserMail();
        String userName = mapper.selectOne(queryWrapper).getUserName();
        String code = verificationCode.get();
        AjaxJson reply = mailService.sendResetMail(code, toMail);
        resetPasswordCode.put(code, userid + ";" + userName);
        return reply;
    }

    /**
     * use code to reset password
     */
    @Override
    public AjaxJson resetPassword(String code, String password) {
        String userInfo;
        userInfo = resetPasswordCode.get(code);
        if (userInfo == null) {
            return AjaxJson.getError("verification code error!");
        }
        User u = new User();
        u.setUserId(userInfo.split(";")[0]);
        u.setUserName(userInfo.split(";")[1]);
        u.setUserPassword(password);
        AjaxJson aj = resetPassword(u);
        if (aj.code == 200) {
            resetPasswordCode.remove(code);
        }
        return aj;
    }

    @Override
    public AjaxJson getUserInformation(String userId) {
        MPJLambdaWrapper<User> mpjLambdaWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .selectCollection(Role.class, UserInfoDTO::getUserPermission)
                .leftJoin(Permission.class, Permission::getUserId, User::getUserId)
                .leftJoin(Role.class, Role::getRoleId, Permission::getRoleId)
                .eq(User::getUserId, userId);
        return AjaxJson.getSuccessData(mapper.selectJoinOne(UserInfoDTO.class, mpjLambdaWrapper));
    }

    public AjaxJson getUserSelfInformation(String userId) {
        MPJLambdaWrapper<User> mpjLambdaWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .select("(SELECT COUNT(st.user_id) AS userId " +
                        "FROM user st " +
                        "left join user theMajor on (st.user_major = theMajor.user_major) " +
                        "where theMajor.user_id = " + userId +
                        " GROUP BY st.user_major) AS userTotal")
                .select("rank() over (partition by user_major order by user_score desc, user_id) as userRank");
        List<Map<String, Object>> resultList = mapper.selectJoinMaps(mpjLambdaWrapper);
        Map<String, Object> result = new HashMap<>();
        for (Map<String, Object> map : resultList) {
            if (map.get("user_id").equals(userId)) {
                result = map;
                break;
            }
        }
        String userRank = result.get("userRank").toString() + "/" + result.get("userTotal");
        result.remove("userRank");
        result.remove("userTotal");
        result.put("user_rank", userRank);
        LambdaUpdateWrapper<User> updateWrapper = new LambdaUpdateWrapper<>();
        updateWrapper.eq(User::getUserId, userId)
                .set(User::getUserRank, userRank);
        mapper.update(null, updateWrapper);
        return AjaxJson.getSuccessData(result);
    }

    @Override
    public boolean isAdmin(String userId) {
        MPJLambdaWrapper<User> mpjLambdaWrapper = new MPJLambdaWrapper<User>()
                .eq(User::getUserId, userId)
                .select(Permission::getPermissionId)
                .leftJoin(Permission.class, Permission::getUserId, User::getUserId)
                .leftJoin(Role.class, Role::getRoleId, Permission::getRoleId)
                .eq(Role::getRoleName, "admin");
        List<Integer> permissionIds = mapper.selectJoinList(Integer.class, mpjLambdaWrapper);
        return !permissionIds.isEmpty();
    }

    @Override
    public boolean isBlack(String userId) {
        MPJLambdaWrapper<User> mpjLambdaWrapper = new MPJLambdaWrapper<User>()
                .eq(User::getUserId, userId)
                .select(Permission::getPermissionId)
                .leftJoin(Permission.class, Permission::getUserId, User::getUserId)
                .leftJoin(Role.class, Role::getRoleId, Permission::getRoleId)
                .eq(Role::getRoleName, "black");
        List<Integer> permissionIds = mapper.selectJoinList(Integer.class, mpjLambdaWrapper);
        return !permissionIds.isEmpty();
    }

    @Override
    public Float countScore(String userId) {
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>()
                .select("sum(course_score * chosen_score) / sum(course_score)")
                .eq(User::getUserId, userId);
        return mapper.selectJoinOne(Float.class, queryWrapper);
    }

    @Override
    public User getUserById(String userId) {
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .eq(User::getUserId, userId);
        return mapper.selectOne(queryWrapper);
    }

    @Override
    public List<User> getRank(String userMajor) {
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>()
                .selectAll(User.class)
                .eq(User::getUserMajor, userMajor)
                .orderByDesc(User::getUserScore)
                .orderByAsc(User::getUserId);
        return mapper.selectList(queryWrapper);
    }

    @Override
    public List<Map<String, Object>> getAllScoreMap(String userId) {
        MPJLambdaWrapper<User> queryWrapper = new MPJLambdaWrapper<User>();
        return mapper.selectJoinMaps(queryWrapper);
    }
}

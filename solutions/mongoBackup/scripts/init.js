rs.status();
db.createUser({user: 'admin', pwd: 'admin', roles: [ { role: "clusterAdmin", db: "admin" }, { role: "userAdminAnyDatabase", db: "admin" } ]});

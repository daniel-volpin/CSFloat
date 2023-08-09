class CSFloat {
  final String itemID;
  final String type;
  final double price;
  final CSItem itemInfo;
  final CSSeller? sellerInfo;

  CSFloat({
    required this.itemID,
    required this.type,
    required this.price,
    required this.itemInfo,
    this.sellerInfo,
  });

  factory CSFloat.fromJson(Map<String, dynamic> json) {
    return CSFloat(
      itemID: json['id'] as String,
      type: json['type'] as String,
      price: (json['price'] as double) / 100.0,
      itemInfo: CSItem.fromJson(json['item']),
      sellerInfo: CSSeller.fromJson(json['seller']),
    );
  }
}

class CSItem {
  final String assetID;
  final dynamic floatValue;
  final dynamic dParam;
  final dynamic isStatTrak;
  final dynamic isSouvenir;
  final dynamic rarity;
  final dynamic quality;
  final dynamic marketHashName;
  final List<CSSticker> stickers;
  final dynamic inspectLink;
  final dynamic itemName;
  final dynamic wearName;

  CSItem({
    required this.assetID,
    required this.floatValue,
    required this.dParam,
    required this.isStatTrak,
    required this.isSouvenir,
    required this.rarity,
    required this.quality,
    required this.marketHashName,
    required this.stickers,
    required this.inspectLink,
    required this.itemName,
    required this.wearName,
  });

  factory CSItem.fromJson(Map<String, dynamic> json) {
    return CSItem(
      assetID: json['asset_id'] as String,
      floatValue: json['float_value'] as dynamic,
      dParam: json['d_param'] as dynamic,
      isStatTrak: json['is_stattrak'] as dynamic,
      isSouvenir: json['is_souvenir'] as dynamic,
      rarity: json['rarity'] as dynamic,
      quality: json['quality'] as dynamic,
      marketHashName: json['market_hash_name'] as dynamic,
      stickers: (json['stickers'] as List<dynamic>?)
        ?.map((stickerJson) => CSSticker.fromJson(stickerJson as Map<String, dynamic>))
        .toList() ?? [],
      inspectLink: json['inspect_link'] as dynamic,
      itemName: json['item_name'] as dynamic,
      wearName: json['wear_name'] as dynamic,
    );
  }
}

class CSSticker {
  final dynamic stickerId;
  final dynamic slot;
  final dynamic iconURL;
  final dynamic name;
  final CSScm scm;

  CSSticker({
    required this.stickerId,
    required this.slot,
    required this.iconURL,
    required this.name,
    required this.scm,
  });

  factory CSSticker.fromJson(Map<String, dynamic> json) {
    return CSSticker(
      stickerId: json['stickerId'] as dynamic ?? {},
      slot: json['slot'] as dynamic ?? {},
      iconURL: json['icon_url'] as dynamic ?? {},
      name: json['name'] as dynamic ?? {},
      scm: CSScm.fromJson(json['scm'] ?? {}),
    );
  }
}

class CSScm {
  final dynamic price;
  final dynamic volume;

  CSScm({
    required this.price,
    required this.volume,
  });

  factory CSScm.fromJson(Map<String, dynamic> json) {
    return CSScm(
      price: json['price'] as dynamic ?? {},
      volume: json['volume'] as dynamic ?? {},
    );
  }
}

class CSSeller {
  final dynamic avatar;
  final dynamic flags;
  final dynamic online;
  final dynamic stallPublic;
  final dynamic steamID;
  final dynamic username;

  CSSeller({
    required this.avatar,
    required this.flags,
    required this.online,
    required this.stallPublic,
    required this.steamID,
    required this.username,
  });

  factory CSSeller.fromJson(Map<String, dynamic> json) {
    return CSSeller(
      avatar: json['avatar'] as dynamic ?? {},
      flags: json['flags'] as dynamic ?? {},
      online: json['online'] as dynamic ?? {},
      stallPublic: json['stall_public'] as dynamic ?? {},
      steamID: json['steam_id'] as dynamic,
      username: json['username'] as dynamic ?? {},
    );
  }
}
